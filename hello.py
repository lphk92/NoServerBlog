from flask import Flask, render_template, request, url_for

import os.path
import markdown2
import json

app = Flask(__name__)

def __url_to_filename(url_str):
    filename = url_str.replace(" ", "").split("/")[-1]
    filename = "./posts/%s.json" % filename
    return filename

def __filename_to_url(filename):
    url_str = filename.strip().split("/")[-1].split(".")[0]
    return url_str

def __title_to_filename(title):
    special_chars = "!@#$%^&*()_+-=/\\}{[]'\";:<>.,"
    filename = ''.join([c for c in title if not c in special_chars])
    filename = "./posts/%s.json" % filename.replace(" ", "-").lower()
    return filename

@app.route("/")
def hello(n=None):
    return render_template("hello.html", name=n, users=["Me", "You", "That Guy"])

@app.route("/list")
def list_posts():
    files = os.listdir("./posts")    
    urls = [__filename_to_url(f) for f in files]
    print "Files: ", files
    print "urls: ", urls
    return render_template("post_list.html",
                           files=files,
                           urls=urls)
    
@app.route("/blog/<post_name>")
def blog_post(post_name):
    filename = __url_to_filename(post_name)
    print "Looking for file:", filename
    if os.path.isfile(filename):
        print "Found file!"
        with open(filename, 'r') as f:
            obj = json.loads(f.read())
            content = markdown2.markdown(obj["content"])
            return render_template("post_pretty.html",
                                   title=obj["title"],
                                   subtitle=obj["subtitle"],
                                   content=content)
    return "Failure"

@app.route("/edit/<post_name>")
def edit_post(post_name=None):
    print "Post Name: ", post_name
    if post_name == None:
        return "We'll manage all posts from here"
    else:
        filename = __url_to_filename(post_name)
        print "Looking for file:", filename
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                obj = json.loads(f.read())
                print "Loaded object: ", obj
                return render_template("edit_post.html",
                                       title=obj["title"],
                                       subtitle=obj["subtitle"],
                                       content=obj["content"])
        else:
            return "No file with name: " + filename

@app.route("/new")
def new_post():
    return render_template("edit_post.html")

@app.route("/execute_post_edit/", methods=["POST"])
def execute_post_edit():
    data = {}
    #data = dict(request.form) # Can pull it all in at once, need to validate data first
    data["title"] = request.form["title"]
    data["subtitle"] = request.form["subtitle"]
    data["content"] = request.form["content"]
    print "Got data from form!"
    print data
    filename = __title_to_filename(data["title"])
    print "Saving to file ", filename
    with open(filename, 'w') as f:
        f.write(json.dumps(data))
    return "Success!"

if __name__ == "__main__":
    app.run(host=os.environ['IP'],port=int(os.environ['PORT']))
