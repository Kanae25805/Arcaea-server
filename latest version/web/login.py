#import sqlite3
from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for)
import functools

bp = Blueprint('login', __name__, url_prefix='/web')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    # 登录
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if username != 'admin' and password != 'admin':
            error = '错误的用户名或密码 Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = 'admin'
            return redirect(url_for('index.index'))

        flash(error)

    return render_template('web/login.html')


@bp.route('/logout')
def logout():
    # 登出
    session.clear()
    flash('成功登出 Successfully log out.')
    return redirect(url_for('index.index'))


def login_required(view):
    # 登录验证，写成了修饰器
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        x = session.get('user_id')
        # 少用户存在验证
        if x is None:
            return redirect(url_for('login.login'))

        g.user = {'user_id': x, 'username': 'admin'}
        return view(**kwargs)

    return wrapped_view
