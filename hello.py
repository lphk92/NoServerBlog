from flask import Flask, render_template, request, url_for

import os
import os.path
import markdown2
import json
from post import Post
import utils
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    posts = Post.getAllPosts()
    latestPost = posts[0]
    for p in posts:
        if p.date > latestPost.date:
            latestPost = p
    return render_template("post_pretty.html", post=p)

@app.route("/list")
def list_posts():
    files = os.listdir("./posts")
    posts = Post.getAllPosts()
    return render_template("post_list.html", posts=posts)

@app.route("/blog/<post_name>")
def show_post(post_name):
    filename = utils.url_to_filename(post_name)
    if os.path.isfile(filename):
        p = Post.readFromFile(filename)
        return render_template("post_pretty.html", post=p)
    return "Failure"

@app.route("/edit/<post_name>")
def edit_post(post_name=None):
    print "Post Name: ", post_name
    if post_name == None:
        return "We'll manage all posts from here"
    else:
        filename = utils.url_to_filename(post_name)
        print "Looking for file:", filename
        if os.path.isfile(filename):
            p = Post.readFromFile(filename)
            return render_template("edit_post.html", post=p)
        else:
            return "No file with name: " + filename

@app.route("/new")
def new_post():
    return render_template("edit_post.html", post=Post())

@app.route("/execute_post_edit/", methods=["POST"])
def execute_post_edit():
    data = {}
    #data = dict(request.form) # Can pull it all in at once, need to validate data first
    data["title"] = request.form["title"]
    data["subtitle"] = request.form["subtitle"]
    data["content"] = request.form["content"]
    data["date"] = request.form["date"]
    print "Got data from form!"
    print data
    filename = utils.title_to_filename(data["title"])
    print "Saving to file ", filename
    with open(filename, 'w') as f:
        f.write(json.dumps(data))
    return "Success!"

if __name__ == "__main__":
    app.run(host=os.environ['IP'], port=int(os.environ['PORT']), debug=True)