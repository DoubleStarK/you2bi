
class VideoNotExistErr(Exception):
    def __init__(self, video_id: str, path=""):
        self.video_id = video_id
        self.path = path

    def __repr__(self):
        return "VideoNotExistErr{video: {}, path: {}}".format(self.video_id, self.path)


class NotLoginErr(Exception):
    def __repr__(self):
        return "NotLoginErr{Please login via: biliup login}"
