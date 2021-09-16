from flask import render_template, flash, url_for, request, current_app
from flask_login import login_required
from app.user.forms import EmptyForm, SearchForm
from app.user_models import User
from app.user import bp


@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user/user_view/user_popup.html', user=user, form=form)


@bp.route('/explore_users', methods=['GET', 'POST'])
@login_required
def explore():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)

    if form.validate_on_submit():
        username = form.username.data
        search = "%{}%".format(username)
        users = User.query.filter(User.username.like(search)).all()
        if users:
            return render_template('user/user_view/all_users.html', title='Explore',
                                   users=users, form=form)
        else:
            flash('User does not exists!')

    users = User.query.order_by(User.username.asc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user.explore', page=users.next_num) \
        if users.has_next else None
    prev_url = url_for('user.explore', page=users.prev_num) \
        if users.has_prev else None
    return render_template('user/user_view/all_users.html', title='Explore',
                           users=users.items, next_url=next_url,
                           prev_url=prev_url, form=form)
