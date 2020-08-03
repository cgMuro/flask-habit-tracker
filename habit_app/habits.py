from flask import Blueprint, redirect, render_template, url_for, request, flash
from habit_app import db, login_manager
from flask_login import current_user, login_required
from habit_app.forms import HabitForm
from habit_app.models import Habit, User

habits = Blueprint('habits', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@habits.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    habits = Habit.query.filter_by(user=current_user).all()
    return render_template('home.html', habits=habits)


@habits.route('/add-habit', methods=['GET', 'POST'])
@login_required
def add_habit():
    form = HabitForm()
    if form.validate_on_submit():
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

@habits.route('/<int:habit_id>/update', methods=['GET', 'POST'])
@login_required
def update_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.user != current_user:
        abort(403)
    form = HabitForm()
    if form.validate_on_submit():
        habit.activity = form.activity.data
        habit.time_spent = time_spent=form.time_spent.data
        habit.description = description=form.description.data
        db.session.commit()
        flash('Activity updated!', 'success')
        return redirect(url_for('habits.home'))
    elif request.method == 'GET':
        form.activity.data = habit.activity
        form.time_spent.data = habit.time_spent
        form.description.data = habit.description
        form.submit.label.text = 'Update activity'
    
    return render_template('add_habit.html', form=form, title='Update activity')

@habits.route('/<int:habit_id>/delete')
@login_required
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.user != current_user:
        abort(403)
    db.session.delete(habit)
    db.session.commit()
    flash(f'"{habit.activity}" has been deleted', 'success')
    return redirect(url_for('habits.home'))