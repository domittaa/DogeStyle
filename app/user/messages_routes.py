from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import current_user, login_required
from app import db
from app.user.forms import MessageForm
from app.models import Message, Notification
from app.user_models import User
from app.user import bp


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('user.user', username=recipient))
    return render_template('user/messages/send_message.html', title='Send Message', form=form, recipient=recipient)


@bp.route('/answer/message/<id>', methods=['GET', 'POST'])
@login_required
def answer_message(id):
    form = MessageForm()
    message = Message.query.filter_by(id=id).first_or_404()
    user = User.query.filter_by(id=message.sender_id).first_or_404()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('user.messages'))
    return render_template('user/messages/send_message.html', title='Send Message', form=form, recipient=user.username)


@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()  # update time = mark as read
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user.messages', page=messages.next_num) if messages.has_next else None
    prev_url = url_for('user.messages', page=messages.prev_num) if messages.has_prev else None
    return render_template('user/messages/messages.html', messages=messages.items, next_url=next_url, prev_url=prev_url)


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)  # only notifications after this time will be returned
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{  # list of notifications for user
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
