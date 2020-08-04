from flask import Blueprint, redirect, render_template, url_for, request, flash
from habit_app import db, login_manager
from flask_login import current_user, login_required
from habit_app.forms import HabitForm
from habit_app.models import Habit, User

# Initialize blueprint
habits = Blueprint('habits', __name__)


# Route: '/'
# Methods: GET 
# Desc: Main page
@habits.route('/')
def home():
    # Redirect user to login page if not authenticated
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Return habits based on the user
    habits = Habit.query.filter_by(user=current_user).all()
    return render_template('home.html', habits=habits)

# Route: '/add-habit'
# Methods: GET, POST 
# Desc: Page with form to add a new habit
@habits.route('/add-habit', methods=['GET', 'POST'])
@login_required  #Requires the user to be logged in
def add_habit():
    form = HabitForm()
    # Validate inputs
    if form.validate_on_submit():
        # Create and then save new habit to database
        habit = Habit(
            activity=form.activity.data,
            time_spent=form.time_spent.data,
            description=form.description.data,
            user=current_user
        )
        db.session.add(habit)
        db.session.commit()
        flash('Activity added!', 'success')
        return redirect(url_for('habits.home'))
    
    return render_template('add_habit.html', form=form, title='Add new activity')

# Route: '/habit_id/update'
# Methods: GET, POST 
# Desc: Page with form to update an existing habit
@habits.route('/<int:habit_id>/update', methods=['GET', 'POST'])
@login_required  #Requires the user to be logged in
def update_habit(habit_id):
    # Check if habit exists
    habit = Habit.query.get_or_404(habit_id)
    if habit.user != current_user:
        abort(403)
    form = HabitForm()
    # Validate inputs
    if form.validate_on_submit():
        habit.activity = form.activity.data
        habit.time_spent = time_spent=form.time_spent.data
        habit.description = description=form.description.data
        db.session.commit()
        flash('Activity updated!', 'success')
        return redirect(url_for('habits.home'))
    elif request.method == 'GET':
        # Populate input fields with the details of the habit that the user want to update
        form.activity.data = habit.activity
        form.time_spent.data = habit.time_spent
        form.description.data = habit.description
        form.submit.label.text = 'Update activity'
    
    return render_template('add_habit.html', form=form, title='Update activity')

# Route: '/habit_id/delete'
# Methods: GET, POST 
# Desc: Deletes a specific habit
@habits.route('/<int:habit_id>/delete')
@login_required  #Requires the user to be logged in
def delete_habit(habit_id):
    # Check if habit exists
    habit = Habit.query.get_or_404(habit_id)
    if habit.user != current_user:
        abort(403)
    # Delete habit from database
    db.session.delete(habit)
    db.session.commit()
    flash(f'"{habit.activity}" has been deleted', 'success')
    return redirect(url_for('habits.home'))