from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "temp key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#create the sqlalchemy object
db = SQLAlchemy(app)

from models import *

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        if request.form['firstButton'] == "Enter my page":
            return redirect(url_for('login'))
        elif request.form['firstButton'] == "Create my User!":
            return redirect(url_for('login'))

    elif request.method == 'GET':
	   return render_template("welcome.html") # render a template

@app.route('/dm_bar', methods=['GET', 'POST'])
@login_required
def dm_bar():

    if request.method == 'POST':
        if request.form['logout'] == "Logout":
            return redirect(url_for('logout'))

    elif request.method == 'GET':
       return render_template("dm_bar.html", posts=posts) # render a template
    

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    users = db.session.query(Users).all()
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')

            return redirect(url_for('dm_bar'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))



#start the server with the 'run()' method
if __name__ == '__main__':
	app.run(debug=True)