from flask import render_template, request
import requests
from app.blueprints.main import main
from flask_login import login_required, current_user
from ...models import User, team


@main.route('/', methods=['GET'])
@login_required 
def home():
    users = User.query.all()
    print(users)
    return render_template('home.html', users=users) 

@main.route('/submit_pokemon', methods=['GET', 'POST'])
@login_required
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
            'pokemon_name': pokemon['forms'][0]['name'],
            'base_experience': pokemon['base_experience'],
            'attack_base_stat': pokemon['stats'][1]['base_stat'],
            'defense_base_stat': pokemon['stats'][2]['base_stat'],
            'front_shiny': pokemon['sprites']['front_shiny']
            }
        else:
            error = 'Invalid entry. Please enter Pokemon name'
            return render_template('submit_pokemon.html', error=error)
        return render_template('submit_pokemon.html', pokemon_data=pokemon_data) 
    
    team_set = set()

    for pokemon in current_user.teams:
        team_set.add(pokemon)
    
    return render_template('submit_pokemon.html', pokemons=pokemons)


    


# @main.route('/catch/<int:pokemon_id>', methods=['GET'])
# @login_required
# def catch_pokemon(pokemon_id):
#     pokemon = Pokemon.query.get(pokemon_id)
#     if current_user.id:
#         pokemon.catch_pokemon()
#     else:
#     return redirect(url_for('pokemon.view_team'))