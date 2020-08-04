from flask import Blueprint, redirect, render_template, url_for, request, flash
from habit_app import db, bcrypt
from flask_login import current_user, login_user, logout_user
from habit_app.forms import RegistrationForm, LoginForm
from habit_app.models import User

# Initialize blueprint
auth = Blueprint('auth', __name__)


# Route: '/register'
# Methods: GET, POST 
# Desc: Allow user to register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect user if already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    # Validate inputs
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create and then save new user to database
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('habits.home'))

    return render_template('register.html', form=form)

# Route: '/login'
# Methods: GET, POST 
# Desc: Allow user to login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect user if already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('habits.home'))

    form = LoginForm()
    # Validate inputs
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # Redirect to the page that the user was trying to access when not logged, if it exists
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('habits.home'))
        else:
            # Handle invalid inputs
            flash('Invalid credentials. Please try again.', 'danger')
        
    return render_template('login.html', form=form)

# Route: '/logout'
# Methods: GET
# Desc: Allow user to logout
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('habits.home'))