from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
# from flask_app.models.project import Project
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# dateFormat = "%#m/%#d/%Y %I:%M %p"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def reg():
    if User.validate_reg(request.form):
        user_id = User.save(request.form)
        print(user_id)
        session["user_id"] = user_id
        return redirect('/dashboard')
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    this_user = User.validate_login(request.form)
    print(this_user)
    if this_user:
        session["user_id"] = this_user.id
        return redirect('/dashboard')
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
