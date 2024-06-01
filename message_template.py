import re
from util import logger

class MessageTemplate:
    '''
                                    Characters              Encoding
    Safe characters                 [0-9a-zA-Z] $-_.+!*'()  No
    Reserved characters             ; / ? : @ = &	        Yes*
    Unsafe characters               Includes the            Yes
                                    blank/empty space and
                                    " < > # % { } | \ ^ ~
                                    [ ] `
    意思是自定义消息模板的时候,最好用Unsafe characters,这样就不会和url里的字符冲突了
    '''
    def __init__(self) -> None:
        '''
        定义消息模板中的一些属性和默认值
        '''
        self.video_url = ''
        self.tid = 21                   # 投稿tid
        self.video_type = 2             # 1自制,2转载
        self.download_only = False      # 仅下载,不上传
        self.trans_video_meta = True    # 翻译title,tag,description
        self.subtitle_from = 'en'       # 视频中语音的语言,会翻译成字幕
        self.subtitle_to = 'zh'         # 想给视频自动添加字幕的语言

    def __pre_check_attr(self):
        for k, v in self.__get_keywords().items():
            try:
                self.__getattribute__(v)
            except AttributeError:
                logger.error('message template wrong: key:{} does not have attribute'.format(k))
    
    def __get_keywords(self)-> dict:
        '''
        在此处定义消息模板到属性的映射
        解释:
            <v:\s*(.*?)\s*>是一个正则表达式,代表匹配消息中的 <v: xxx >
        其中xxx左右的空格可有可无,并将xxx赋值给video_url
        '''
        return {
            r'<v:\s*(.*?)\s*>': 'video_url',
            r'<vt:\s*(.*?)\s*>': 'video_type',
            r'<tid:\s*(.*?)\s*>': 'tid',
            r'<trans:\s*(.*?)\s*>': 'trans_video_meta',
            r'<sf:\s*(.*?)\s*>': 'subtitle_from',
            r'<st:\s*(.*?)\s*>': 'subtitle_to',
            r'<dlo:\s*(.*?)\s*>': 'download_only',
        }

    def set_from_message(self, message: str):
        self.__pre_check_attr()
        for k, v in self.__get_keywords().items():
            pattern = re.compile(k, re.DOTALL)
            match_res = pattern.findall(message)
            if len(match_res) == 1:
                self.__setattr__(v, self.__convert_params(match_res[0]))

    def __convert_params(self, dirty: str) -> any:
        if dirty.lower() == 'true':
            return True
        elif dirty.lower() == 'false':
            return False
        try:
            return int(dirty)
        except ValueError:
            try:
                return float(dirty)
            except ValueError:
                return dirty

if __name__ == '__main__':
    t = MessageTemplate()
    t.set_from_message('foo <v:http://xxx> <vt:2> <tid: 20> <trans: True > <sf:en><st:cn> <dlo:True> bar')
    print(t.__dict__)
