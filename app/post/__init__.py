from flask import Blueprint

bp = Blueprint('post', __name__)

from app.post import add_post_routes, comments_routes, tags_routes, post_like_routes, post_view_routes
