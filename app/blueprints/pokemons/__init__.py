from flask import Blueprint 

pokemons = Blueprint('pokemons', __name__, template_folder='pokemons_templates', url_prefix='/pokemons')

from app.blueprints.pokemons import routes 