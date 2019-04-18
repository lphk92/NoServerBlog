import os
import json
import markdown2
import utils


class Post(object):
    def __init__(self, title="", subtitle="", date="", content="", url=""):
        self.title = title
        self.subtitle = subtitle
        self.date = date
        self.content = content
        self.md_content = markdown2.markdown(self.content)
        self.url = url

    @staticmethod
    def readFromFile(filename):
        with open(filename, 'r') as f:
            obj = json.loads(f.read())
            return Post(obj["title"],
                        obj["subtitle"],
                        obj["date"],
                        obj["content"],
                        utils.filename_to_url(filename))

    @staticmethod
    def getAllPosts():
        files = os.listdir("./posts")
        posts = list()
        for filename in files:
            posts.append(Post.readFromFile("./posts/" + filename))
        return posts

    def writeToFile(self, filename):
        data = dict()
        data["title"] = self.title
        data["subtitle"] = self.subtitle
        data["date"] = self.date
        data["content"] = self.content
        with open(filename, 'w') as f:
            f.write(json.dumps(data))
