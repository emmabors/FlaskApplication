from flask import render_template, request, flash, redirect, url_for
import requests
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app import app
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/submit_pokemon', methods=['GET', 'POST'])
def submit_pokemon():
    pokemons = ['Pikachu', 'Bulbasaur', 'Squirtle', 'Charizard']
    print(request.method)
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name')
        print(pokemon_name)
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
        response = requests.get(url)
        if response.ok:
            pokemon = response.json()
            pokemon_data = {
            'Pokemon': pokemon['forms'][0]['name'],
            'Base_experience': pokemon['base_experience'],
            'Sprite': pokemon['sprites']['back_default']
            }
        else:
            error = 'Invalid entry. Please enter Pokemon name'
            return render_template('submit_pokemon.html', error=error)
        return render_template('submit_pokemon.html', pokemon_data=pokemon_data) 
    return render_template('submit_pokemon.html', pokemons=pokemons)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Successfully logged in. Hello, {queried_user.first_name}!', 'success')
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or password.'     
            flash(f'{error}', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
    
@app.route('/logout', methods=['GET'])
def logout():
    if current_user:
        logout_user()
        flash('You have succesfully logged out.', 'warning')
        return redirect(url_for('login'))
    


         
    

  
