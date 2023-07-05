from flask import render_template, g, session, request, url_for, Blueprint, redirect, flash
from werkzeug.exceptions import abort 

from flaskr.auth import login_required
from flaskr.db import get_db 

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db() 
    posts = db.execute('SELECT p.id, title, body, created, author_id, username'
                       ' FROM post p JOIN user u on p.author_id = u.id'
                       ' ORDER BY created DESC').fetchall()
    return render_template('blog/index.html', posts=posts) 

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
            db=get_db()
            db.execute('INSERT INTO POST (title, body, author_id) VALUES (?, ?, ?)',
                       (title, body, g.user['id']))
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    db = get_db()
    post = db.execute('SELECT p.id, title, body, created, author_id, username'
                      ' FROM post p JOIN user u on p.author_id=u.id'
                      ' WHERE p.id = ?', (id,)).fetchone()
    if post is None:
        abort(404, f'Post id {id} does not exist.') #404 means NOT FOUND

    if check_author and post['author_id'] != g.user['id']:
        abort(403) # 403 means FORBIDDEN

    return post

@bp.route('/<int:id>/update', methods = ('POST', 'GET'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None 

        if not title:
            error = "Title is required"

        if error is not None:
             flash(error)
        else:
            db = get_db()
            db.execute('UPDATE post set title = ?, body = ? WHERE id = ?', (title, body, id))
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete',  methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post where id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

