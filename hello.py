from flask import Flask, render_template, request, url_for

import os.path
import markdown2
import json

app = Flask(__name__)

@app.route("/")
def hello(n=None):
    return render_template("hello.html", name=n, users=["Me", "You", "That Guy"])

@app.route("/blog/<post_name>")
def blog_post(post_name):
    #TODO: sanitize input
    post_name = post_name.strip().split(" ")[-1]
    filename = "./posts/%s.md" % post_name
    print "Looking for file:", filename
    if os.path.isfile(filename):
        print "Found file!"
        with open(filename, 'r') as f:
            content = f.read()
            content = markdown2.markdown(content)
            return render_template("post_pretty.html",
                                   post_name=post_name.replace("-", " ").title(),
                                   content=content)
    return "Failure"

@app.route("/edit/<post_name>")
def edit_post(post_name):
    return render_template("edit_post.html")

@app.route("/execute_post_edit/", methods=["POST"])
def execute_post_edit():
    data = {}
    data["title"] = request.form["title"]
    data["subtitle"] = request.form["subtitle"]
    data["content"] = request.form["content"]
    print "Got data from form!"
    print data
    return "Success!"

if __name__ == "__main__":
    app.run()
