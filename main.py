from flask import Flask, render_template, request, url_for, redirect

from post import Post


app = Flask(__name__)


@app.route("/")
def index():
    posts = Post.get_all_posts()
    return render_template("post_pretty.html", post=posts[0])


@app.route("/list")
def list_posts():
    posts = Post.get_all_posts()
    return render_template("post_list.html", posts=posts)


@app.route("/blog/<post_id>")
def show_post(post_id):
    p = Post.read_from_file(post_id)
    return render_template("post_pretty.html", post=p)


@app.route("/edit/<post_id>")
def edit_post(post_id=None):
    print("Post Id: ", post_id)
    if post_id is None:
        return "We'll manage all posts from here"
    else:
        p = Post.get_post(post_id)
        return render_template("edit_post.html", post=p)


@app.route("/new")
def new_post():
    return render_template("edit_post.html", post=Post())


@app.route("/execute_post_edit/<post_id>", methods=["POST"])
def execute_post_edit(post_id):
    data = dict(request.form)
    post = Post(post_id=post_id, **data)
    print(f"Got editted post: {post}")

    post.write_to_file()
    return redirect(url_for('show_post', post_id=post_id))


if __name__ == "__main__":
    #app.run(host=os.environ['IP'], port=int(os.environ['PORT']), debug=True) # noqa
    app.run(debug=True)
