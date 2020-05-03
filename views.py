from app import app
from models import *
from flask import render_template
from flask import request, redirect
from flask import url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_admin import AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
import requests
import json

# Lets your application and Flask-Login work together
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Trainer.query.get(int(user_id))


#@app.route('/')
#def index():
#    trainer = Trainer.query.filter_by(name='Corn').first()
#    login_user(trainer)
#    return 'You are now logged in!'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        trainer_name = request.form['trainer']
        password = request.form['password']
        new_trainer = Trainer(name=trainer_name, password=password)
        try:
            db.session.add(new_trainer)
            db.session.commit()
            redirect('/')
        except Exception as e:
            print(e)
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logmein', methods=['POST', 'GET'])
def logmein():
    username = request.form['trainer']
    password = request.form['password']

    user = Trainer.query.filter_by(name=username, password=password).first()

    if not user:
        return '<h1> Wrong username/password!'
    
    login_user(user)

    return f'<h1>Hello, {user.name.title()}'

   

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out!'


@app.route('/poke_list', methods=['POST', 'GET'])
@login_required
def add_pokemon():
    if request.method == 'POST':
        p_name = request.form['pokemon_name']
        new_pokemon = Pokemon(name=p_name, owner=current_user)

        try:
            db.session.add(new_pokemon)
            db.session.commit()
            return redirect('/poke_list')
        except Exception as e:
            print(e)
            raise
    else:
        return render_template('greet_trainer.html', user=current_user)


@app.route('/delete', methods=['POST', 'GET'])
@login_required
def delete_pokemon():
    # Delete pokemon from list.
    # Get pokemon id
    # If user clicks delete,
    # It will remove id from database
    if request.method == 'POST':
        pokemon_id = request.form['pokemon_id']
        delete_pokemon = PokemonBelt.query.filter_by(id=pokemon_id).first()
        
        try:
            db.session.delete(delete_pokemon)
            db.session.commit()
            return redirect('/pokemonbelt')
        except Exception as e:
            raise
            print(e)

@app.route('/pokemons', methods=['POST', 'GET'])
@login_required
def pokemons():
    
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=151")

    allPokemon = response.json()
    #print(allPokemon)

    pokemonData = []
    
    
    for url in allPokemon['results']:
        pokemon_url = url['url']
        poke_response = requests.get(pokemon_url)
        pokeData = poke_response.json()

        pokeInfo = {
            'id': pokeData['id'],
            'name': pokeData['name'],
            'types': fetchPokemonTypes(pokeData['types']),
        
        }
        #print(pokeInfo)
        pokemonData.append(pokeInfo)


    if request.method == "POST":
        pokeName = request.form['pokename']
        adding_to_storage = PokemonBelt(name=pokeName, owner=current_user)
        try:
            db.session.add(adding_to_storage)
            db.session.commit()
            return redirect('/pokemons')
        except Exception as e:
            print(e)
            raise
    else:

           
        return render_template('pokemon_list.html', pokemonData=pokemonData)

def fetchPokemonTypes(types):
    # return 1-2 type names
    # iterate through types and fetch the names and store them somewhere
    type_names = []
    for type in types:
        type_name = type['type']['name']
        print(f"Type name {type_name}")
        type_names.append(type_name)

    return type_names    

@app.route('/test', methods=['POST', 'GET'])
@login_required
def test():

    if request.method == "POST":
        pokemon_ID = request.form['pokemon_id']
        pokeName = request.form['pokemon_name']
        print(pokeName)
        print("Hellooooooooo!")
        

        if len(current_user.poke_belt) != 6:
            adding_to_belt = PokemonBelt(name=pokeName, pokeid=pokemon_ID, owner=current_user)
            try:
                db.session.add(adding_to_belt)
                db.session.commit()
                return redirect('/pokemons')
            except Exception as e:
                print(e)
                raise e
        else:
            return redirect('/pokemonbelt')
    else:  
        return render_template('pokemon_list.html')





@app.route('/pokemonbelt')
@login_required
def pokemon_storage():
    return render_template('pokemon_belt.html', user=current_user)







"""
class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inasseccible_callback(self, name, **kwargs):
        return redirect('/login')

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(AdminView(Trainer, db.session))
admin.add_view(AdminView(Pokemon, db.session))
"""

