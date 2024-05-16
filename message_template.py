import re

class MessageTemplate:
    '''
                                    Characters              Encoding
    Safe characters                 [0-9a-zA-Z] $-_.+!*'()  No
    Reserved characters             ; / ? : @ = &	        Yes*
    Unsafe characters               Includes the            Yes
                                    blank/empty space and
                                    " < > # % { } | \ ^ ~
                                    [ ] `
    '''
    def __init__(self) -> None:
        '''
        定义消息模板中的一些属性
        '''
        self.video_url = ''
        self.tid = 0
        self.trans_title_tag = True
        self.trans_subtitle_from = 'en' # 视频中语音的语言,会翻译成字幕
        self.add_subtitle_lang = 'zh'   # 想给视频自动添加字幕的语言

    def get_mapping(self):
        return {
            '\[v:(.*?)\]': self.video_url,
            '<t(\d+)>': self.tid,
            '<trans(.*?)>': self.trans_title_tag,
            '<sf(.*?)>': self.trans_subtitle_from,
            '<st(.*?)>': self.add_subtitle_lang,
        }
    def set_from_message(self, message: str):
        for pattern, attr in self.get_mapping().items():
            match = re.match(pattern, message)
            if match:
                attr = match.group(1)

if __name__ == '__main__':
    t = MessageTemplate()
    t.set_from_message('[v:http://youtube.com] <t1><transTrue><sfen><stzh>')


