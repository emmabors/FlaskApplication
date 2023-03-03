from flask import render_template, request
import requests
from app.forms import LoginForm
from app import app 

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
        if email in app.config.get('REGISTERED_USERS') and password == app.config.get('REGISTERED_USERS').get(email).get('password'):
            return f'Successfully logged in. Hello, {app.config.get("REGISTERED_USERS").get(email).get("name")}' 
        else:
            error = 'Invalid email or password.'     
            return error
    print('Not validated')
    return render_template('login.html', form=form)

         
    

  
