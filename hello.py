from flask import Flask, render_template

import os.path
import markdown2

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

if __name__ == "__main__":
    app.run()
