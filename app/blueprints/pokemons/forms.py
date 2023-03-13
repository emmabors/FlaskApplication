from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

class PokemonForm(FlaskForm):
    pokemon_name = StringField('Pokemon Name:', validators=[DataRequired()])
    base_experience = StringField('Base Experience:', validators=[DataRequired()])
    attack_base_stat = StringField('Attack Base Stat:', validators=[DataRequired()])
    defense_base_stat = StringField('Defense Base Stat:', validators=[DataRequired()])
    sprite = StringField('Front Shiny:', validators=[DataRequired()])
    