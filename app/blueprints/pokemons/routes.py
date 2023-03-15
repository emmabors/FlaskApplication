from flask import render_template, request, flash, redirect, url_for
import requests
from app.blueprints.pokemons.forms import PokemonForm
from app.models import Pokemon, User
from app.blueprints.pokemons import pokemons
from flask_login import current_user, login_required

@pokemons.route('/view_team', methods=['GET'])
@login_required 
def view_team():
    pokemons = current_user.teams
    return render_template('view_team.html', pokemons=pokemons)

@pokemons.route('/<int:pokemon_id>', methods=['GET'])
@login_required
def view_single_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon:
        return render_template('view_single_pokemon.html', pokemon=pokemon)
    else:
        flash('This pokemon does not exist', 'danger')
        return redirect(url_for('pokemons.view_team'))  

@pokemons.route('/catch/<pokemon_name>')
@login_required
def catch(pokemon_name):
    pokemon = Pokemon.query.filter_by(pokemon_name=pokemon_name).first()
    print('here')
    if pokemon:
        print('inside if')
        current_user.catch_pokemon(pokemon)
        flash(f'You caught {{pokemon_name}}!', 'success')
        return redirect(url_for('main.submit_pokemon'))
    else:
        print('inside else')
        pokemon_name = pokemon_name
        print(pokemon_name)
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
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
            poke = Pokemon()
            poke.from_dict(pokemon_data)
            poke.save_to_db()
            current_user.catch_pokemon(poke)
            flash(f'You caught {{"pokemon_name"}}!', 'success')
            return redirect(url_for('main.submit_pokemon'))
    return redirect(url_for('main.submit_pokemon'))

@pokemons.route('/remove/<int:pokemon_id>')
@login_required
def remove_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if current_user.id == pokemon.user_id:
        pokemon.remove_pokemon()
        flash(f'You removed {{Pokemon.pokemon_name.title()}} from your team.', 'warning')
        return redirect(url_for('pokemons.view_team'))
    return redirect(url_for('pokemons.view_team'))

@pokemons.route('/battlefield/<user_id>', methods = ['GET'])
@login_required 
def battlefield(user_id):
    user = User.query.get(user_id)
    myteam = current_user.teams
    otherteam = user.teams 
    return render_template('battlefield.html', myteam=myteam, otherteam=otherteam)




    
