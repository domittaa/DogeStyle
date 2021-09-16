from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app import db
from app.user.forms import EmptyForm
from app.user_models import User
from app.user import bp


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user.user', username=username))
    else:
        return redirect(url_for('post.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('post.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user.user', username=username))
    else:
        return redirect(url_for('post.index'))


@bp.route('/followers/<id>', methods=['GET', 'POST'])
@login_required
def followers(id):
    user = User.query.filter_by(id=id).first_or_404()
    followers = user.followers.all()
    return render_template('user/user_view/followers.html', followers=followers, user=user, title="followers")


@bp.route('/following/<id>', methods=['GET', 'POST'])
@login_required
def following(id):
    user = User.query.filter_by(id=id).first_or_404()
    following = user.followed.all()
    return render_template('user/user_view/following.html', following=following, user=user, title="following")
