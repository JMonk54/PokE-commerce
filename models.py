from app import db
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView

class Trainer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    pokemons = db.relationship('Pokemon', backref='owner')
    poke_belt = db.relationship('PokemonBelt', backref='owner')


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    owner_id = db.Column(db.Integer, db.ForeignKey('trainer.id'))


class PokemonBelt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    pokeid = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('trainer.id'))