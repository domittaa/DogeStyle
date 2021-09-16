from flask import render_template, flash, redirect, send_from_directory, url_for, request, current_app
from flask_login import current_user, login_required
from app import db
from app.post.forms import PostForm
from app.models import Post, Comment, Tag
from app.post import bp
import os
from werkzeug.utils import secure_filename
import imghdr, collections

from app.post.post_like_routes import redirect_url


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    files = os.listdir(current_app.config['UPLOAD_PATH'])
    if form.validate_on_submit():
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                flash('Invalid image!')
                return redirect(url_for('post.index'))
            uploaded_file.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
        post = Post(body=form.post.data, author=current_user, filename=filename)
        db.session.add(post)
        tags_list = form.tag.data
        tags_list_split = tags_list.split()
        tags_list_seperated = [x.strip() for x in tags_list_split]
        unique_tags = [item for item, count in collections.Counter(tags_list_seperated).items() if count > 0]
        for tag in unique_tags:
            tags = Tag(name=tag, post=post)
            db.session.add(tags)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('post.index'))

    page = request.args.get('page', 1, type=int)
    list = current_user.followed_posts()
    id = [tuple[0] for tuple in list]

    posts = Post.query.filter(Post.id.in_(id)).group_by(Post.id).order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('post.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('post.index', page=posts.prev_num) if posts.has_prev else None

    return render_template('post/create/index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url, files=files)


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@bp.route('/uploads/<filename>')
@login_required
def upload(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)


@bp.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    Comment.query.filter(Comment.post_id == id).delete()
    Tag.query.filter(Tag.post_id == id).delete()
    post = Post.query.filter_by(id=id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted!')
    return redirect(redirect_url())


@bp.route('/edit/post/<id>',  methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    tags = Tag.query.filter_by(post_id=id).all()
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.post.data
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                flash('Invalid image!')
                return redirect(url_for('post.edit_post', id=id))
            uploaded_file.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
            Post.query.filter_by(id=id).update({"filename": (filename)})
            db.session.commit()
        for tag in tags:
            Tag.query.filter_by(name=tag.name).delete()
            db.session.commit()
        tags_list = form.tag.data
        tags_list_seperated = tags_list.replace("", "").split(",")
        for tag in tags_list_seperated:
            tags = Tag(name=tag, post=post)
            db.session.add(tags)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('post.view_post', id=post.id))
    elif request.method == 'GET':
        form.post.data = post.body
        tags = [tag.name for tag in post.tags]
        form.tag.data = ', '.join([str(elem) for elem in tags])
    return render_template('post/create/edit_post.html', form=form, title='Edit Post')





