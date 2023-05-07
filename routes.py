import datetime
import base64
from flask import render_template, url_for, flash, redirect, request, abort
from atitube import app, db, bcrypt
from atitube.forms import RegisterForm, LoginForm, UpdateAccount, VideoForm
from atitube.models import User, Video
from flask_login import login_user, current_user, logout_user, login_required
from flask import send_file


@app.route("/")
def home():
    videos = Video.query.all()
    return render_template('home.html', title='home', videos=videos)


@app.route('/about')
def about():
    return render_template('about.html', title='about')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, Email=form.Email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'המשתמש נוצר בהצלחה', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'התחברת בהצלחה', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('התהליך נכשל, נסה שוב', 'danger')
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.Email = form.Email.data
        db.session.commit()
        flash('פרטי החשבון עודכנו בהצלחה!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.Email.data = current_user.Email
    return render_template('account.html', title='Account', form=form)


@app.route("/video/new", methods=['GET', 'POST'])
@login_required
def newVideo():
    form = VideoForm()
    if form.validate_on_submit():
        file = request.files.get('video')
        data = file.read()
        videoo = Video(name=form.name.data, description=form.description.data, video_file=data, author=current_user, date=datetime.datetime.now())
        db.session.add(videoo)
        db.session.commit()
        flash("הסרטן הועלה בהצלחה!",'success')
        return redirect(url_for('home'))
    return render_template("create_video.html", title='New Video', form=form,
                           legend='Create Video')


@app.route("/video/<int:video_id>", methods=['GET', 'POST'])
@login_required
def show_video(video_id):
    video = Video.query.get_or_404(video_id)
    return render_template('video.html', title=video.name, video=video, base64=base64)


@app.route("/video/<int:video_id>/update", methods=['GET', 'POST'])
@login_required
def update_video(video_id):
    videoo = Video.query.get_or_404(video_id)
    if videoo.author != current_user:
        abort(403)
    form = VideoForm()
    data = videoo.video_file
    videoo.video_file = data
    if form.validate_on_submit():
        videoo.name = form.name.data
        videoo.description = form.description.data
        form.video.data = data
        db.session.commit()
        flash('!המידע על הסרטון עודכן בהצלחה', 'success')
        return redirect(url_for('show_video', video_id=videoo.id))
    elif request.method == 'GET':
        form.name.data = videoo.name
        form.description.data = videoo.description
    return render_template("create_video.html", title='Update Video', form=form,
                           legend='Update Video')


@app.route("/video/<int:video_id>/delete", methods=['POST'])
@login_required
def delete_video(video_id):
    videoo = Video.query.get_or_404(video_id)
    if videoo.author != current_user:
        abort(403)
    db.session.delete(videoo)
    db.session.commit()
    flash("הסרטון נמחק", 'success')
    return redirect(url_for('home'))