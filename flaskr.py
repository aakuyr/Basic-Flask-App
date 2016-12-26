import os
import sqlite3
from flask import Flask, render_template, redirect, abort, flash, g 

#Application configuration
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE = os.path.join(os.curdir, 'flaskr.db'),
    SECRET_KEY = 'sai',
    USERNAME = 'root',
    PASSWORD = 'admin'
    ) 
)

app.config.from_envvar('FLASKR_SETTINGS',silent=True)

#Connect to specified database 
def connect_db():
    rv = sqlite3.connect( app.config['DATABASE'] )
    rv.row_factory = sqlite3.Row
    return rv

#Get the database connection for a particular app instance
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#Initialize the database
@app.cli.command('init')
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    print('Initialized')

#CLose the database after application is done
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#Show the complaints
@app.route('/')
def show_complaints():
    db = get_db();
    cur = db.execute('select * from complaints')
    complaints = cur.fetchall()
    return render_template('com.html', complaints=complaints)
