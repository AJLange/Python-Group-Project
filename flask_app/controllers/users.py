from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask_app.models.album import Album
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/registration')
def registration():
    return render_template('register.html')


@app.route('/register', methods=["POST"])
def register():
    print(request.form)
    if not User.validate_reg(request.form):
        return redirect('/')
    else:  # no errors
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": pw_hash
        }
        user_id = User.save(data)
        session['user_id'] = user_id
    return redirect('/dashboard')


@app.route('/user_login')
def login_page():

    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login():
    print(request.form)
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Wrong password!", "login")
        return redirect('/')
    else:  # no errors
        session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.get_by_id(data), albums=Album.get_all(), liked_albums=Album.get_liked_albums(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.errorhandler(404)
def not_found(e):
    return "Sorry! No response! Try again!"


if __name__ == "__main__":   # Ensure this file is being run directly and not from a different module
    app.run(debug=True)    # Run the app in debug mode.
