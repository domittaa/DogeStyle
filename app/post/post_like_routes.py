from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.models import Post, PostLike, PostDislike
from app.post import bp


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


@bp.route('/like/<id>/<action>', methods=['GET', 'POST'])
@login_required
def like_post(id, action):
    post = Post.query.filter_by(id=id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
        flash('You like this post')
        return redirect(redirect_url())
    if action == 'unlike':
        current_user.unlike_post(post)
        flash('You do not like this post anymore.')
        db.session.commit()
    return redirect(redirect_url())


@bp.route('/dislike/<id>/<action>', methods=['GET', 'POST'])
@login_required
def dislike_post(id, action):
    post = Post.query.filter_by(id=id).first_or_404()
    if action == 'dislike':
        current_user.dislike_post(post)
        db.session.commit()
        flash('You do not like this post.')
        return redirect(redirect_url())
    if action == 'delete_dislike':
        current_user.delete_dislike(post)
        flash('You deleted your dislike for this post.')
        db.session.commit()
    return redirect(redirect_url())


@bp.route('/view_dislikes/<id>', methods=['GET', 'POST'])
@login_required
def view_dislikes(id):
    post = Post.query.filter_by(id=id).first_or_404()
    dislikes = PostDislike.query.filter_by(post_id=post.id).all()
    return render_template('post/likes/view_dislikes.html', post=post, dislikes=dislikes, title="Dislikes")


@bp.route('/view_likes/<id>', methods=['GET', 'POST'])
@login_required
def view_likes(id):
    post = Post.query.filter_by(id=id).first_or_404()
    likes = PostLike.query.filter_by(post_id=post.id)
    return render_template('post/likes/view_likes.html', post=post, likes=likes, title="Likes")