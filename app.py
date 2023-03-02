from flask import Flask, render_template, request
import requests

app = Flask(__name__)

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
            return 'Invalid entry. Please enter Pokemon name'
        return render_template('submit_pokemon.html', pokemon_data=pokemon_data)
    return render_template('submit_pokemon.html', pokemons=pokemons)

  
