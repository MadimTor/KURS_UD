import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.cursor().execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.DatabaseError as e:
                if e.args[2] == 335544665:  #isc_unique_key_violation
                    error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')




@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.cursor().execute('SELECT * FROM users WHERE username = ?', (username,) ).fetchonemap()
        type = 0
        if user is None:
            error = 'Неверное имя пользователя.'
        elif not check_password_hash(user['password'], password):
            error = 'Неверный пароль.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['user_type'] = user['role']
            session['id'] = user['user_id']
            if user['role'] == 1:
                return redirect(url_for('student.about', mark = 0))
            if user['role'] == 2:
                return redirect(url_for('teacher.subs'))
            if user['role'] == 3:
                return redirect(url_for('admin.main'))
        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    user_type = session.get('user_type')
    id = session.get('id')
    if user_type == 1:
        if user_id is None:
            g.user = None
        else:
            g.user = get_db().cursor().execute('SELECT * FROM student WHERE id = ?', (id,)).fetchonemap()
    if user_type == 2:
        if user_id is None:
            g.user = None
        else:
            g.user = get_db().cursor().execute('SELECT * FROM teacher WHERE id = ?', (id,)).fetchonemap()
    if user_type == 3:
        if user_id is None:
            g.user = None
        else:
            g.user = get_db().cursor().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchonemap()        


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user_type = session.get('user_type')
        if  user_type != 3:
            session.clear()
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view