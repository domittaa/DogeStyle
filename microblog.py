from app import create_app, db
from app.models import Post, Notification, Message, Comment,\
    PostLike, PostDislike, CommentLike, CommentDislike, Tag
from app.user_models import User

app = create_app()


@app.shell_context_processor  # model classes automatically imported when flask shell starts
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message, 'Notification': Notification,
            'Comment': Comment, 'PostLike': PostLike, 'PostDislike': PostDislike, 'CommentLike': CommentLike,
            'CommentDislike': CommentDislike, 'Tag': Tag}
