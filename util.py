import hashlib
import logging

from PIL import Image
from googletrans import Translator
from httpx import Timeout

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s | %(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)


def has_chs(title: str):
    for i in title:
        if u'\u4e00' <= i <= u'\u9fa5':
            return True
    return False


def get_uuid(raw: str) -> str:
    harsher = hashlib.md5()
    harsher.update(str(raw).encode("utf-8"))
    return harsher.hexdigest()


translator = Translator(service_urls=[
    'translate.google.com',
    'translate.google.co.kr',
],
    timeout=Timeout(10.0)
)


def translate_to_chinese(plain_text: str) -> str:
    retry_times = 0
    while True:
        try:
            translated = translator.translate(plain_text, src='auto', dest='zh-cn').text
            return translated
        except Exception as e:
            retry_times += 1
            if retry_times > 5:
                break
            continue
