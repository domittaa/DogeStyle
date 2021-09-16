from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt
from flask import current_app
import json
from app.models import Notification, Post, PostLike, PostDislike, CommentLike, CommentDislike, Message

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(240))
    followed = db.relationship('User',  # right side entity of the relationship, the left side is a parent class- also User
                               secondary=followers,  # configures the association table that is used for this relationship
                               primaryjoin=(  # indicates the condition that links left side entity with association table
                                followers.c.follower_id == id),  # join condition is that user ID matches follower_id
                               secondaryjoin=(  # indicates the condition that links the right side entity with the association table
                                followers.c.followed_id == id),
                               backref=db.backref('followers',  # defines how this relationship will be accessed from the right side
                                                  lazy='dynamic'), lazy='dynamic')  # dynamic sets up query not to run until specifically requested
    liked = db.relationship('PostLike', foreign_keys='PostLike.user_id', backref='user', lazy='dynamic')
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    dislikes = db.relationship('PostDislike', backref='user', lazy='dynamic')
    comment_likes = db.relationship('CommentLike', backref='user', lazy='dynamic')
    comment_dislikes = db.relationship('CommentDislike', backref='user', lazy='dynamic')

    def __repr__(self):  # tells python how to print object of this class
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=mp&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.with_entities(Post.id).join(  # join Post table with followers table
            followers, (followers.c.followed_id == Post.user_id)
        ).filter(  # select the post that have this user as a follower
            followers.c.follower_id == self.id)
        own = Post.query.with_entities(Post.id).filter_by(user_id=self.id)
        return followed.union(own).all()

    def like_post(self, post):
        if not self.liked_posts(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.liked_posts(post):
            PostLike.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def liked_posts(self, post):
        return PostLike.query.filter(PostLike.user_id == self.id, PostLike.post_id == post.id).count() > 0

    def dislike_post(self, post):
        if not self.disliked_posts(post):
            dislike = PostDislike(user_id=self.id, post_id=post.id)
            db.session.add(dislike)

    def delete_dislike(self, post):
        if self.disliked_posts(post):
            PostDislike.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def disliked_posts(self, post):
        return PostDislike.query.filter(PostDislike.user_id == self.id, PostDislike.post_id == post.id).count() > 0

    def liked_comments(self, comment):
        return CommentLike.query.filter(CommentLike.user_id == self.id, CommentLike.comment_id == comment.id).count() >0

    def like_comment(self, comment):
        if not self.liked_comments(comment):
            like = CommentLike(user_id=self.id, comment_id=comment.id)
            db.session.add(like)

    def unlike_comment(self, comment):
        CommentLike.query.filter_by(user_id=self.id, comment_id=comment.id).delete()

    def disliked_comments(self, comment):
        return CommentDislike.query.filter(CommentDislike.user_id == self.id, CommentDislike.comment_id == comment.id).count() > 0

    def dislike_comment(self, comment):
        if not self.disliked_comments(comment):
            dislike = CommentDislike(user_id=self.id, comment_id=comment.id)
            db.session.add(dislike)

    def delete_dislike_comment(self, comment):
        if self.disliked_comments(comment):
            CommentDislike.query.filter_by(user_id=self.id, comment_id=comment.id).delete()

    def get_reset_password_token(self, expires_in=600):  # tokens generation function, token is valid for 10 minutes
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')  # returns JWT token as string

    @staticmethod  # can be invoked directly from the class, do not receive the class as first argument
    def verify_reset_password_token(token):  # takes a token and tries to decode it
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return  # if validation fails an exception will be raised and None is returned
        return User.query.get(id)  # if the token is valid user ID is returned

    def new_messages(self):  # returns how many unread messages the user has
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):  # adds notification to database
        self.notifications.filter_by(name=name).delete()  # delete notification if notification with the same name already exists
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
