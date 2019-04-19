from pathlib import Path
import datetime
import json
import markdown2
import math
import time

import config as config


posts_root = Path(config.data_root) / 'posts'
trash_root = Path(config.data_root) / 'trash'

if not posts_root.exists():
    posts_root.mkdir()

if not trash_root.exists():
    trash_root.mkdir()


def get_file(post_id, trash=False):
    if trash:
        return trash_root / f'{post_id}.json'
    return posts_root / f'{post_id}.json'


def generate_id():
    return int(math.floor(time.time() * 1e6))

def today():
    return datetime.datetime.now().date().strftime("%Y-%m-%d")


class Post(object):
    defaults = {
        "post_id": None,
        "title": "",
        "subtitle": "",
        "date": None,
        "content": ""
    }

    def __init__(self, **kwargs):
        self.__dict__ = dict(Post.defaults)
        self.__dict__.update(kwargs)

        if self.post_id is None:
            self.post_id = generate_id()

        if self.date is None:
            self.date = today()

    @property
    def md_content(self):
        return markdown2.markdown(self.content)

    def write_to_file(self):
        data = dict(self.__dict__)

        f = get_file(self.post_id)
        f.write_text(json.dumps(data))

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
        # We can sort by post_id because it is a time, it will sort it be creation time
        return sorted(posts, key=lambda x: int(x.post_id), reverse=True)

    @staticmethod
    def get_post(post_id):
        f = get_file(post_id)
        return Post(**json.loads(f.read_text()))

    @staticmethod
    def delete(post_id):
        get_file(post_id).rename(get_file(post_id, trash=True))
