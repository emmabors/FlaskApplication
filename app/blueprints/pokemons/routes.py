from flask import render_template, request, flash, redirect, url_for
import requests
from app.blueprints.pokemons.forms import PokemonForm
from app.models import Pokemon
from app.blueprints.pokemons import pokemons
from flask_login import current_user, login_required

# @pokemon.route('/create_post', methods=['GET', 'POST'])
# @login_required
# def create_post():
#     form = PostForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         new_post_data = { 
#             'img_url': form.img_url.data,
#             'title': form.title.data,
#             'caption': form.caption.data,
#             'user_id': current_user.id
#         }
#         new_post = Post()
#         new_post.from_dict(new_post_data)
#         new_post.save_to_db()
#         flash('Your post has been made!', 'success')
#         return redirect(url_for('posts.view_posts'))
#     return render_template('create_post.html', form=form)

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
    if pokemon:
        current_user.remove_pokemon(pokemon)
        flash(f'You removed {{Pokemon.pokemon_name.title()}} from your team.', 'warning')
    return redirect(url_for('main.home'))

# @posts.route('/update/<int:post_id>', methods=['GET', 'POST'])
# @login_required 
# def update_post(post_id):
#     form = PostForm()
#     post = Post.query.get(post_id)
#     if request.method == 'POST' and form.validate_on_submit():
#         new_post_data = { 
#             'img_url': form.img_url.data,
#             'title': form.title.data,
#             'caption': form.caption.data,
#             'user_id': current_user.id
#         }
#         post.from_dict(new_post_data)
#         post.update_to_db()
#         flash('Profile is updated!', 'success')
#         return redirect(url_for('main.home'))
#     return render_template('edit_profile.html', form=form)

@pokemons.route('/delete/<int:pokemon_id>', methods=['GET'])
@login_required
def delete_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if current_user.id == pokemon.user_id:
        post.delete_pokemon()
    else:
        flash('🐍 You do not have permission to delete another players pokemon', 'danger')
    return redirect(url_for('pokemons.view_team'))

    
