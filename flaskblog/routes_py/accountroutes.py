from flask import flash, redirect, render_template, url_for, request
from flaskblog.models import Post, User
from flaskblog.forms import LoginForm, RegistrationForm, UpdateNameForm, UpdatePfpForm, SmartPasswordForm#, RequestResetForm, ResetPasswordForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets #Savepicture
from PIL import Image #Savepicture
import os #Savepicture


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created uwu', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title=' - Register on Aniani!', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Failed. Nice Meme.', 'danger')
    return render_template('login.html', title=' - Log In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/pfp', pic_fn)
    output_size = (250,250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pic_path)
    
    return pic_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateNameForm()
    form2 = UpdatePfpForm()
    form3 = SmartPasswordForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your username has been updated.', 'success')
        return redirect(url_for('account'))
    elif form2.validate_on_submit():
        if form2.picture.data:
            pic_file = save_picture(form2.picture.data)
            current_user.image_file = pic_file
            db.session.commit()
    elif form3.is_submitted(): #validation issue
        if bcrypt.check_password_hash(current_user.password, form3.password.data): #everythingworks fine below
            newhash = bcrypt.generate_password_hash(form3.newpassword.data).decode('utf-8')
            current_user.password = newhash
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    image_file = url_for('static', filename='pfp/' + current_user.image_file)
    return render_template('account.html', title=' - Account', image_file=image_file, form=form, form3=form3, form2=form2)

@app.route('/profile/<string:username>')
def user_profile(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_profile.html', posts=posts, user=user)

@app.route('/notsmartreset', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route('/passwordreset', methods=['GET', 'POST'])
def reset_password():
    pass