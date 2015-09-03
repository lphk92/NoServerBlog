import json
import markdown2

class Post(object):
    def __init__(self, title="", subtitle="", date="", content=""):
        self.title = title
        self.subtitle = subtitle
        self.date = date
        self.content = content
        self.md_content = markdown2.markdown(self.content)

    @staticmethod
    def readFromFile(self, filename):
        with open(filename, 'r') as f:
            obj = json.loads(f.read())
            return Post(obj["title"],
                        obj["subtitle"],
                        obj["date"],
                        obj["content"])

    def writeToFile(self, filename):
        data = dict()
        data["title"] = self.title
        data["subtitle"] = self.subtitle
        data["date"] = self.date
        data["content"] = self.content
        with open (filename, 'w') as f:
            f.write(json.dumps(data))
