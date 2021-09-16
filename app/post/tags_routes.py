from datetime import datetime
from flask import render_template, url_for, request, current_app
from flask_login import login_required
from app.models import Post, Tag
from app.post import bp
from sqlalchemy import func, text, extract


@bp.route('/tag/<name>', methods=['GET', 'POST'])
@login_required
def view_posts_with_tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    page = request.args.get('page', 1, type=int)
    post = Post.query.join(Tag, (Tag.post_id == Post.id)).filter(Tag.name == name).order_by(
        Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('post.view_posts_with_tag', name=tag.name, page=post.next_num) if post.has_next else None
    prev_url = url_for('post.view_posts_with_tag', name=tag.name, page=post.prev_num) if post.has_prev else None

    return render_template('post/tags/tags.html', post=post.items, tag=tag,
                           next_url=next_url, prev_url=prev_url,
                           title="Tag")


@bp.route('/popular/tags/<time>', methods=['GET', 'POST'])
@login_required
def popular_tags(time):
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

    top = Tag.query.with_entities(Tag.name.label('tag'), func.count(
        Tag.name).label('cnt')).filter(
        Tag.post_id.in_(post_id)).group_by(
        Tag.name).order_by(text('cnt DESC')).limit(10)

    result = []
    for r in top:
        row = r._asdict()
        result.append(row)

    return render_template('post/tags/popular_tags.html', result=result)
