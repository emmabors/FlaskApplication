from app import db, login
from flask_login import UserMixin 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

team = db.Table(
    'team',
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String)
    base_experience = db.Column(db.Integer)
    attack_base_stat = db.Column(db.Integer)
    defense_base_stat = db.Column(db.Integer)
    front_shiny = db.Column(db.String)

    def from_dict(self, data):
        self.pokemon_name = data['pokemon_name']
        self.base_experience = data['base_experience']
        self.attack_base_stat = data['attack_base_stat']
        self.defense_base_stat = data['defense_base_stat']
        self.front_shiny = data['front_shiny']

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_post(self):
        db.session.delete(self)
        db.session.commit()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    teams = db.relationship('Pokemon', 
        secondary = team,
        backref = 'team',
        lazy = 'dynamic'
    )

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])


    def update_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']        

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

    def update_to_db(self):
        db.session.commit()

    def catch_pokemon(self, user):
        self.teams.append(user)
        db.session.commit()

    def remove_pokemon(self, user):
        self.teams.remove(user)
        db.session.commit()

         

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

        

