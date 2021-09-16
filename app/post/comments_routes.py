from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import db
from app.post.forms import CommentForm
from app.models import Comment, CommentLike, CommentDislike
from app.user_models import User
from app.post import bp


@bp.route('/delete/comment/<id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    flash('Comment has been deleted.')
    return redirect(url_for('post.view_post', id=comment.post_id))


@bp.route('/edit/comment/<id>', methods=['GET', 'POST'])
@login_required
def edit_comment(id):
    comment = Comment.query.filter_by(id=id).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        comment.body = form.body.data
        db.session.commit()
        flash('Your changes has been saved.')
        return redirect(url_for('post.view_post', id=comment.post_id))
    elif request.method == 'GET':
        form.body.data = comment.body
    return render_template('post/comments/edit_comment.html', form=form, title="Edit Comment")


@bp.route('/view/comments/<id>', methods=['GET', 'POST'])
@login_required
def view_comments(id):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(id=id).first_or_404()
    comments = Comment.query.join(User, (User.id == Comment.user_id)).filter(Comment.user_id == user.id).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('post.view_comments', id=id, page=comments.next_num) if comments.has_next else None
    prev_url = url_for('post.view_comments', id=id, page=comments.prev_num) if comments.has_prev else None
    return render_template('post/comments/view_comments.html', comments=comments.items, user=user, title='Comments',
                           next_url=next_url, prev_url=prev_url)


@bp.route('/like_comment/<id>/<action>', methods=['GET', 'POST'])
@login_required
def like_comment(id, action):
    comment = Comment.query.filter_by(id=id).first_or_404()
    if action == 'like':
        current_user.like_comment(comment)
        db.session.commit()
        flash("You like this comment.")
        return redirect(url_for('post.view_post', id=comment.post_id))
    if action == 'unlike':
        current_user.unlike_comment(comment)
        db.session.commit()
        flash("You do not like this comment anymore.")
    return redirect(url_for('post.view_post', id=comment.post_id))


@bp.route('/dislike_comment/<id>/<action>', methods=['GET', 'POST'])
@login_required
def dislike_comment(id, action):
    comment = Comment.query.filter_by(id=id).first_or_404()
    if action == 'dislike':
        current_user.dislike_comment(comment)
        db.session.commit()
        flash("You dislike this comment.")
        return redirect(url_for('post.view_post', id=comment.post_id))
    if action == 'delete_dislike':
        current_user.delete_dislike_comment(comment)
        db.session.commit()
        flash("You deleted your dislike.")
    return redirect(url_for('post.view_post', id=comment.post_id))


@bp.route('/view_comment_dislikes/<id>', methods=['GET', 'POST'])
@login_required
def view_comment_dislikes(id):
    comment = Comment.query.filter_by(id=id).first_or_404()
    dislikes = CommentDislike.query.filter_by(comment_id=comment.id).all()
    return render_template('post/likes/view_dislikes.html', comment=comment, dislikes=dislikes, title="Dislikes")


@bp.route('/view_comment_likes/<id>', methods=['GET', 'POST'])
@login_required
def view_comment_likes(id):
    comment = Comment.query.filter_by(id=id).first_or_404()
    likes = CommentLike.query.filter_by(comment_id=comment.id)
    return render_template('post/likes/view_likes.html', comment=comment, likes=likes, title="Likes")
