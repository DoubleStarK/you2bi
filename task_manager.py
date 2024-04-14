import json
import re
import time

import requests
from typing import List

from downloader import VideoTransfer

from util import logger


class BiliTaskManager:
    def __init__(self,
                 sender_uid,
                 receiver_uid,
                 cookie_file='./cookie.json',
                 download_record_file='./data.json',
                 chat_history_size=1,
                 refresh_interval_seconds=120):
        self.refresh_interval_seconds = refresh_interval_seconds
        self.cookie_file = cookie_file
        self.download_record_file = download_record_file
        self.chat_history_size = chat_history_size
        self.receiver_uid = receiver_uid
        self.sender_uid = sender_uid
        self.chat_api = "https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs?session_type=1" \
                        "&sender_device_id=1&size={}&build=0&mobi_app=web&talker_id={}".format(self.chat_history_size,
                                                                                               self.receiver_uid)

    def get_cookie(self) -> str:
        try:
            text = open(self.cookie_file).read()
            json_obj = json.loads(text)
            cookie_list = json_obj["data"]["cookie_info"]["cookies"]

            for cookie in cookie_list:
                if cookie["name"] == "SESSDATA":
                    sess_data = cookie["value"]
                    logger.debug("Get bilibili cookie success: {}".format(sess_data))
                    return sess_data
        except Exception as e:
            logger.error("Get bilibili cookie failed: {}".format(e))

    def query_bilibili_api(self, url: str):
        r = requests.get(url, headers={
            "User-Agent": "Apifox/1.0.0 (https://www.apifox.cn)",
            "Accept-Encoding": None,
            "Accept": None,
            "Connection": None,
            "Cookie": "SESSDATA=" + self.get_cookie()
        })
        return r.json()

    def save_record(self, data):
        with open(self.download_record_file, "w") as f:
            f.write(json.dumps(data))

    def read_records(self):
        with open(self.download_record_file, "r") as f:
            return json.loads(f.read())

    @staticmethod
    def match_url(url) -> str:
        match = re.search(r'\$(.*?)\$', url)
        if match:
            return match.group(1)
        return ''

    @staticmethod
    def match_tid(url) -> str:
        match = re.search(r'<(.*?)>', url)
        if match:
            return match.group(1)
        return ''

    def get_tasks(self) -> dict:
        task_paris = {}
        resp = self.query_bilibili_api(self.chat_api)
        message_list = resp["data"]["messages"]

        for msg_obj in message_list:
            if str(msg_obj["sender_uid"]) == self.sender_uid and int(msg_obj["msg_type"]) == 1:
                video_url, tid = self.match_url(msg_obj["content"]), self.match_tid(msg_obj["content"])
                video_url = video_url.replace("\\/", "/")
                if len(video_url) > 0:
                    logger.debug("Task info from message: video_url {} to tid {}.".format(video_url, tid))
                    task_paris[video_url] = tid
                else:
                    continue

        return task_paris

    def run_task(self):
        try:
            task_history = self.read_records()
        except Exception as e:
            task_history = dict()

        try:
            while True:
                task_list = self.get_tasks()
                for video_url, tid in task_list.items():
                    if video_url in task_history.keys():
                        logger.debug("Skip already done task: video_url {} to tid {}.".format(video_url, tid))
                        continue
                    logger.debug("New task: video_url {} to tid {}.".format(video_url, tid))

                    transferer = VideoTransfer(video_url, tid)
                    transferer.download_youtube()
                    transferer.upload_bilibili()

                    task_history[video_url] = tid
                    time.sleep(self.refresh_interval_seconds)

                time.sleep(self.refresh_interval_seconds)
        except RuntimeError as e:
            logger.error('{}'.format(e))
        except Exception as e:
            logger.error('{}'.format(e))
        finally:
            self.save_record(task_history)


if __name__ == '__main__':
    sender = '384542669'
    receiver = '3546592707610853'
    BiliTaskManager(sender, receiver, refresh_interval_seconds=10).run_task()