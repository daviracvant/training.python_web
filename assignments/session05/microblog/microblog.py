from flask import Flask, g, render_template, request, url_for, redirect, flash, session
import sqlite3
from contextlib import closing

app = Flask(__name__)

app.config.from_pyfile('microblog.cfg')


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_database_connection():
    db = getattr(g, 'db', None)
    if db is None:
        g.db = db = connect_db()
    return db


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def write_entry(title, text):
    con = get_database_connection()
    con.execute('insert into entries (title, text) values (?, ?)',
                [title, text])
    con.commit()


def get_all_entries():
    con = get_database_connection()
    cur = con.execute('SELECT title, text FROM entries ORDER BY id DESC')
    return [dict(title=row[0], text=row[1]) for row in cur.fetchall()]


#a function to check credential.
def is_logged_in(username, password):
    log_in = True
    if username != app.config['USERNAME']:
        log_in = False
    elif password != app.config['PASSWORD']:
        log_in = False
    return log_in


@app.route('/')
def show_entries():
    entries = get_all_entries()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    try:
        write_entry(request.form['title'], request.form['text'])
    except sqlite3.Error as db_error:
        flash("Error occurs: %s" % db_error.args[0])
    else:
        flash("New entry posted")
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        logged_in = is_logged_in(request.form['username'], request.form['password'])
        if logged_in:
            session['logged_in'] = True
            flash("You are logged in as %s" % request.form['username'])
            return redirect(url_for('show_entries'))
        else:
            flash("Invalid Credential.")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    flash("You have logged out")
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(debug=True)
