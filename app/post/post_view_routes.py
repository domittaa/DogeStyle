from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import db
from app.post.forms import CommentForm
from app.models import Post, Comment, PostLike, PostDislike, Tag
from app.user_models import User
from app.post import bp
from sqlalchemy import func, text, extract
from datetime import datetime
from hashlib import md5


@bp.route('/explore_posts')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('post.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('post.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('post/post_view/explore.html', title='Explore',
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/post/<id>', methods=['GET', 'POST'])
@login_required
def view_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, user=current_user, post=post, parent_id=form.parentId.data)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment is now live!')
        return redirect(url_for('post.view_post', id=id))

    tags = Tag.query.filter_by(post=post).all()

    page = request.args.get('page', 1, type=int)
    comments = Comment.query.join(Post, (Post.id == Comment.post_id)).order_by(
        Comment.timestamp.desc()).filter(
        post.id == Comment.post_id).paginate(
        page, current_app.config['COMMENTS_PER_PAGE'], False)
    next_url = url_for('post.view_post', id=id, page=comments.next_num) if comments.has_next else None
    prev_url = url_for('post.view_post', id=id, page=comments.prev_num) if comments.has_prev else None

    return render_template('post/post_view/view_post.html', post=post, comments=comments.items, form=form, tags=tags,
                           prev_url=prev_url, next_url=next_url, title='View Post')


def build_avatar(email, size=64):
    digest = md5(email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?d=mp&s={}'.format(digest, size)


@bp.route('/popular/posts/<time>', methods=['GET', 'POST'])
@login_required
def popular_posts(time):
    now = datetime.utcnow()

    if time == 'this_hour':
        post = Post.query.with_entities(Post.id).filter(extract('year', Post.timestamp) == now.year,
                                                        extract('month', Post.timestamp) == now.month,
                                                        extract('day', Post.timestamp) == now.day,
                                                        extract('hour', Post.timestamp) == now.hour).all()
    elif time == 'this_day':
        post = Post.query.with_entities(Post.id).filter(extract('year', Post.timestamp) == now.year,
                                                        extract('month', Post.timestamp) == now.month,
                                                        extract('day', Post.timestamp) == now.day).all()
    elif time == 'this_month':
        post = Post.query.with_entities(Post.id).filter(extract('year', Post.timestamp) == now.year,
                                                        extract('month', Post.timestamp) == now.month).all()
    elif time == 'this_year':
        post = Post.query.with_entities(Post.id).filter(extract('year', Post.timestamp) == now.year).all()
    elif time == 'all_time':
        post = Post.query.with_entities(Post.id).all()

    post_id = [item for id in post for item in id]

    post_likes = Post.query.with_entities(Post.id, Post.body, Post.timestamp,
                                          User.username, User.image, User.id.label('user_id'), User.email,
                                          func.count(PostLike.post_id).label('likes'),
                                          func.count(PostDislike.post_id).label('dislikes')).join(
        PostLike, Post.id == PostLike.post_id, isouter=True).join(
        User, Post.user_id == User.id).join(
        PostDislike, Post.id == PostDislike.post_id, isouter=True).filter(
        Post.id.in_(post_id)).group_by(Post.id).order_by(text('likes DESC')).limit(10)

    result = []
    for r in post_likes:
        row = r._asdict()
        row["avatar"] = build_avatar(row["email"])
        result.append(row)

    return render_template('post/post_view/popular_posts.html', result=result)