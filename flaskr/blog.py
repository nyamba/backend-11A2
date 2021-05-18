from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flask import jsonify
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/reaction/<int:post_id>')
def reaction(post_id):
    db = get_db()
    data = db.execute(
        'SELECT * FROM reaction WHERE post_id=' + str(post_id)).fetchone()

    if data is None:
        return jsonify([])

    ss = {
        'like': data['like'],
        'dislike': data['dislike'],
        'post_id': data['post_id']
    }

    return jsonify(ss)


@bp.route('/set/like/<int:post_id>/<int:count>')
def set_like(post_id, count):
    db = get_db()
    db.execute(
        'UPDATE reaction SET like = ?'
        ' WHERE post_id = ?',
        (count, post_id)
    )
    db.commit()

    return 'ok'


@bp.route('/set/dislike/<int:post_id>/<int:count>')
def set_dislike(post_id, count):
    db = get_db()
    db.execute(
        'UPDATE reaction SET dislike = ?'
        ' WHERE post_id = ?',
        (count, post_id)
    )
    db.commit()

    return 'ok'


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/detail/<int:post_id>')
def detail(post_id):
    db = get_db()
    post = db.execute(
        'SELECT * FROM post WHERE id=' + str(post_id)).fetchone()
    return render_template('blog/detail.html', post=post)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.detail', post_id=id))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
