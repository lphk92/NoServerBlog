from pathlib import Path
import datetime
import json
import markdown2
import math
import time

import config as config


posts_root = Path(config.data_root) / 'posts'


def get_file(post_id):
    return posts_root / f'{post_id}.json'


def today():
    return datetime.datetime.now().date().strftime("%Y-%m-%d")


class Post(object):
    def __init__(self, post_id=None, title="", subtitle="", date=None, content=""):
        self.post_id = post_id if post_id is not None else str(math.floor(time.time() * 1e6))
        self.title = title
        self.subtitle = subtitle
        self.date = date if date is not None else today()
        self.content = content
        self.md_content = markdown2.markdown(self.content)

    @staticmethod
    def read_from_file(post_id):
        f = get_file(post_id)
        if not f.exists():
            raise ValueError(f"No post saved with post_id {post_id}")
        obj = json.loads(f.read_text())
        return Post(**obj)

    @staticmethod
    def get_all_posts():
        posts = [Post(**json.loads(f.read_text())) for f in posts_root.iterdir()]
        return sorted(posts, key=lambda x: x.date, reverse=True)

    @staticmethod
    def get_post(post_id):
        f = get_file(post_id)
        return Post(**json.loads(f.read_text()))

    def write_to_file(self):
        data = dict()
        data["title"] = self.title
        data["subtitle"] = self.subtitle
        data["date"] = self.date
        data["content"] = self.content
        data["post_id"] = self.post_id

        f = get_file(self.post_id)
        f.write_text(json.dumps(data))
