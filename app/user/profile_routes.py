from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import db
from app.user.forms import EditProfileForm, EmptyForm
from app.models import Post
from app.user_models import User
from app.user import bp
import os
from werkzeug.utils import secure_filename
from app.post.add_post_routes import validate_image
from datetime import datetime


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user/profile/user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    files = os.listdir(current_app.config['UPLOAD_AVATAR_PATH'])
    if form.validate_on_submit():
        uploaded_file = request.files['avatar']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                flash('Invalid image!')
                return redirect(url_for('user.edit_profile'))
            uploaded_file.save(os.path.join(current_app.config['UPLOAD_AVATAR_PATH'], str(current_user.id)))
        User.query.filter(User.id == current_user.id).update({"username": (form.username.data),
                                                              "about_me": (form.about_me.data),
                                                              "image": (filename)})
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('user/profile/edit_profile.html', title='Edit Profile', form=form, files=files)

