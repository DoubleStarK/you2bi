import os
import re
import shutil
import requests
import yt_dlp
from PIL import Image

import util
from typing import List
from util import logger


class VideoTransfer:
    def __init__(self,
                 video_url: str,
                 bili_tid: str,
                 translate_desc: bool = True,
                 translate_title: bool = True,
                 translate_tags: bool = False,
                 convert_cover_format: bool = True,
                 remove_after_download: bool = True,
                 skip_if_cover_exist: bool = True,
                 skip_if_video_exist: bool = True,
                 proxy: str = None):
        self._folder_name = 'downloads'
        self._default_bili_tid = '21'
        self._video_uuid = util.get_uuid(video_url)
        self._download_dir = '{}/{}'.format(self._folder_name, self._video_uuid)

        self._video_title = ''
        self._video_author = ''
        self._video_id = ''
        self._video_description = ''
        self._video_tags = []
        self._video_cover_url = ''
        self._video_url = video_url

        self.TID = self._default_bili_tid if bili_tid == '' else bili_tid

        self.translate_desc = translate_desc
        self.translate_title = translate_title
        self.translate_tags = translate_tags
        self.convert_cover_format = convert_cover_format
        self.proxy = proxy
        self.remove_after_download = remove_after_download
        self.skip_if_cover_exist = skip_if_cover_exist
        self.skip_if_video_exist = skip_if_video_exist

    def get_video_path(self):
        if len(self._video_id) == 0:
            raise FileNotFoundError(self._video_id)
        return '{}/{}.mp4'.format(self._download_dir, self._video_id)

    def get_cover_path(self):
        return '{}/cover.jpeg'.format(self._download_dir)

    def download_video(self):
        self.make_video_dir(remove_existing_dir=False)
        ydl_opts = {
            # outtmpl 格式化下载后的文件名，避免默认文件名太长无法保存
            'outtmpl': self._download_dir + '/%(id)s.mp4'
        }
        if self.skip_if_video_exist and os.path.exists(self.get_video_path()):
            logger.debug("Video exist, skip download...")
            return

        logger.debug("Start download: {} into {}...".format(self._video_url, self.get_video_path()))
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self._video_url])
                logger.debug("End download: {} into {}.".format(self._video_url, self.get_video_path()))
        except Exception as e:
            raise e

    def download_image(self, image_url: str) -> str:
        image_folder = self._download_dir
        webp_file_name = image_folder + "/cover.webp"
        jpeg_file_name = image_folder + "/cover.jpeg"

        if os.path.exists(webp_file_name):
            logger.debug("Cover exist, skip download...")
        else:
            r = requests.get(image_url, stream=True)
            f = open(webp_file_name, "wb")
            logger.debug("Start download image: {} into {}...".format(image_url, image_folder))
            # chunk是指定每次写入的大小，每次只写了100kb
            for chunk in r.iter_content(chunk_size=102400):
                if chunk:
                    f.write(chunk)
            logger.debug("End download image: {} into {}.".format(image_url, image_folder))

        if self.convert_cover_format and not os.path.exists(jpeg_file_name):
            logger.debug("Start converting webp to jpeg...")
            VideoTransfer.cover_webp_to_jpg(webp_file_name, jpeg_file_name)
            logger.debug("Done converting webp to jpeg.")
        return jpeg_file_name

    @staticmethod
    def cover_webp_to_jpg(webp_path: str, jpg_path: str):
        """
        将webp格式的图片转换为jpg格式的图片
        :param webp_path: webp格式的图片路径
        :param jpg_path: jpg格式的图片路径
        :return: None
        """
        try:
            im = Image.open(webp_path).convert('RGB')
            im.save(jpg_path, 'jpeg')
        except Exception as e:
            raise e
        finally:
            im.close()

    def get_video_meta(self):
        ydl_opts = {
            'proxy': self.proxy,
            'logger': logger,
        }

        logger.debug("Getting meta info of: {}".format(self._video_url))
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_meta_info = ydl.extract_info(self._video_url, download=False)
                self._video_title = video_meta_info['title']
                self._video_author = video_meta_info['uploader']
                self._video_id = video_meta_info['id']
                self._video_description = video_meta_info['description']
                self._video_tags = video_meta_info['tags']
                self._video_cover_url = video_meta_info['thumbnail']
                logger.debug("Done getting meta info of: {}".format(self._video_url))
                return video_meta_info
        except Exception as e:
            raise e

    def make_video_dir(self, remove_existing_dir=False):
        try:
            os.makedirs(self._download_dir)
        except FileExistsError:
            if remove_existing_dir:
                logger.warning("Dir {} exists, removing...".format(self._download_dir))
                shutil.rmtree(self._download_dir)
                logger.warning("Dir {} removed, removing...".format(self._download_dir))
            else:
                logger.warning("Ignored existing folder {}.".format(self._download_dir))

    def get_video_abs_path(self, video_id: str):
        for root, dirs, files in os.walk(self._download_dir):
            for file in files:
                if file.find(video_id) != -1:
                    return os.path.join(root, file)

    @staticmethod
    def batch_translate(raw_text_arr: List[str]) -> List[str]:
        if len(raw_text_arr) > 1:
            raw = '\n'.join(raw_text_arr)
        elif len(raw_text_arr) == 0:
            return []
        else:
            raw = raw_text_arr[0]
        logger.debug("Start to translate...")
        result = util.translate_to_chinese(raw)
        logger.debug("Done translating: origin=[{}] -> result=[{}].".format(raw, result))

        result_arr = result.split('\n')
        if len(result_arr) != len(raw_text_arr):
            logger.warning("Batch translate is not correct, using original...")
            return raw_text_arr
        return result_arr

    @staticmethod
    def cut_tags(tags: List[str]) -> List[str]:
        for i, tag in enumerate(tags):
            tags[i] = tag[:20].strip()
        return tags

    def download_youtube(self) -> bool:
        self.get_video_meta()
        self.download_video()
        self.download_image(self._video_cover_url)

    def upload_bilibili(self) -> bool:
        self._video_tags.append(self._video_author)
        self._video_tags.append("搬运")
        self._video_tags.append("油管")
        self._video_tags.append("youtube")
        self._video_tags = self._video_tags[:12]

        if not util.has_chs(self._video_title):
            self._video_title = VideoTransfer.batch_translate([self._video_title])[0]
            self._video_title = self._video_title.strip()
        if not util.has_chs(self._video_description):
            self._video_description = VideoTransfer.batch_translate([self._video_description])[0]
            self._video_description = self._video_description.strip()
            tags = VideoTransfer.cut_tags(self._video_tags)
            self._video_tags = VideoTransfer.batch_translate(tags)

        self._video_title = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a\u3040-\u31FF\uFF00"
                                   u"-\uFFA0\u0020"
                                   u"\u3000])",
                                   '', self._video_title)

        if not os.path.exists("cookie.json"):
            raise RuntimeError

        command = ("./biliup upload "
                   + " --v " + repr(self.get_video_path())
                   + " --cover " + repr(self.get_cover_path())
                   + " --title " + repr(self._video_title[:80])
                   + " --desc " + repr(self._video_description[:200])
                   + " --t 2 "
                   + " --tid " + repr(self.TID)
                   + " --tags " + repr(','.join(self._video_tags))
                   + " --source " + repr(self._video_url)
                   )
        logger.debug("Start to using biliup, command: {}".format(command))
        biliup_output = "\n".join(os.popen(command).readlines())
        logger.debug("Done calling biliup, result: {}".format(biliup_output))

        if biliup_output.find("100%") == -1:
            if biliup_output.find("重复") == -1:
                logger.debug(
                    "投稿失败,是bug或biliup出了问题。ask issues on https://github.com/Quandong-Zhang/youtube-trans-bot/issues or "
                    "https://github.com/ForgQi/biliup-rs/issues ")
            else:
                logger.debug("这个视频好像之前投过了...")
                if self.remove_after_download:
                    shutil.rmtree(self._download_dir)

            return False
        else:
            logger.debug("投稿成功!")
            if self.remove_after_download:
                shutil.rmtree(self._download_dir)

            return True


if __name__ == '__main__':
    downloader = VideoTransfer(video_url="https://youtu.be/Q4YUB2GK_sw?si=4VitFjLnLrlSz4gK", bili_tid="21")
    downloader.download_youtube()
    downloader.upload_bilibili()
