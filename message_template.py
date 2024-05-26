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
        定义消息模板中的一些属性
        '''
        self.video_url = ''
        self.tid = 0
        self.download_only = False
        self.trans_title_tag = True
        self.subtitle_from = 'en' # 视频中语音的语言,会翻译成字幕
        self.subtitle_to = 'zh'   # 想给视频自动添加字幕的语言
        self.__pre_check_attr()

    def __pre_check_attr(self):
        for k, v in self.get_keywords().items():
            try:
                self.__getattribute__(v)
            except AttributeError:
                logger.error('message template wrong: key:{} does not have attribute'.format(k))
    
    def get_keywords(self)-> dict:
        '''
        在此处定义消息模板到属性的映射
        解释:
            <v:\s*(.*?)\s*>是一个正则表达式,代表匹配消息中的 <v: xxx >
        其中xxx左右的空格可有可无,并将xxx赋值给video_url
        '''
        return {
            r'<v:\s*(.*?)\s*>': 'video_url',
            r'<t:\s*(.*?)\s*>': 'tid',
            r'<ttt:\s*(.*?)\s*>': 'trans_title_tag',
            r'<sf:\s*(.*?)\s*>': 'subtitle_from',
            r'<sl:\s*(.*?)\s*>': 'subtitle_to',
            r'<dlo:\s*(.*?)\s*>': 'download_only',
        }

    def set_from_message(self, message: str):
        for k, v in self.get_keywords().items():
            pattern = re.compile(k, re.DOTALL)
            match_res = pattern.findall(message)
            if len(match_res) == 1:
                self.__setattr__(v, self.convert_params(match_res[0]))

    def convert_params(self, dirty: str) -> any:
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
    t.set_from_message('<t:1> <v:2> <ttt: True> <tsf: en >   <asl: cn>')
    print(t.__dict__)
