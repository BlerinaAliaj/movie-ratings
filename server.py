"""Movie Ratings."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    a = jsonify([1,3])
    # return a
    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register', methods=["GET"])
def register_page():
    """Page that asks users for login information"""

    return render_template("register.html")


@app.route('/login', methods=["GET"])
def login_page():
    """Page that asks users for login information"""

    return render_template("login_page.html", error="")


@app.route('/register_form', methods=["POST"])
def register():
    """Verifies that user login exists."""

    email = request.form.get('email')
    password = request.form.get('password')
    age = request.form.get('age')
    zipcode = request.form.get('zipcode')

    query_user = User.query.filter_by(email=email).first()

    if not query_user:
        user = User(email=email, password=password, age=age, zipcode=zipcode)
        db.session.add(user)
        db.session.commit()

    return redirect('/')


@app.route('/verify_login', methods=["POST"])
def verify_login():
    """Verifies that user login exists."""

    email = request.form.get('email')
    password = request.form.get('password')

    query_user = User.query.filter_by(email=email).one()

    if query_user:
        user_pass = query_user.password

        if password == user_pass:
            flash('You have successfully logged in.')
            return redirect('/')

        else:
            error = "Your username and password are not correct."
            return render_template("login_page.html", error=error)


##################### FIX THIS!!!
    else:
        flash("Sorry, that username doesn't exist. Please register a new account.")
        return render_template("login_page.html", error=error)


        # return redirect("/login", error=error)
    # except ValueError:
    #     ('Your username and password combination is not correct.')




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')
