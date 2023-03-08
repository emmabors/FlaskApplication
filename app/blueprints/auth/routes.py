from flask import render_template, request, flash, redirect, url_for
from app.blueprints.auth.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
from app.blueprints.auth import auth
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user, login_required

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Successfully logged in. Hello, {queried_user.first_name}!', 'success')
            return redirect(url_for('main.home'))
        else:
            error = 'Invalid email or password.'     
            flash(f'{error}', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data = { 
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': form.password.data
        }
        new_user = User()
        new_user.from_dict(new_user_data)
        new_user.save_to_db()
        flash('You have succesfully registered!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
    
@auth.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data = { 
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': current_user.password
        }
        queried_user = User.query.filter_by(email=new_user_data['email']).first()
        if queried_user:
            current_user.from_dict(new_user_data)
            current_user.save_to_db()
            flash('Profile is updated!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Must have an existing account with registered email to make changes', 'warning')
    return render_template('edit_profile.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have succesfully logged out.', 'warning')
        return redirect(url_for('auth.login'))
