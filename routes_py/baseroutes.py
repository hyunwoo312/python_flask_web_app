from flask import render_template, request
from flaskblog.models import Post
from flaskblog import app


@app.route('/')
@app.route('/nexus')#homebro
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)#10
    return render_template('home.html', posts=posts)


@app.route('/pylon')
def about():
    return render_template('about.html', title=' - About')
