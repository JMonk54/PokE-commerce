import requests
import json
import pprint

from models import Trainer, PokemonBelt
from flask_admin.contrib.sqla import ModelView

"""
response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=151")


allPokemon = response.json()





pokeName = []

for names in allPokemon['results']:
    pokemon_name = names['name']
    pokeName.append(pokemon_name)




pokemonURL = []
for url in allPokemon['results']:
    pokemon_url = url['url']
    pokemonURL.append(pokemon_url)
    


POKEMONS = []

def fetchTypes(types):
    for pokeTypes in types:
        pokeType = pokeTypes['type']
        print(pokeType)
        return pokeType
        

for url in pokemonURL:
    response = requests.get(url)
    pokeData = response.json()
    #print(pokeData['types'])


    pokeInfo = {
    'id': pokeData['id'],
    'name': pokeData['name'],
    'types': fetchTypes(pokeData['types']),
    }
    #print(pokeInfo['id'])
    #print(pokeInfo['name'])
    #print(pokeInfo['types'])
    POKEMONS.append(pokeInfo)

#print(POKEMONS[1])






 















pokedex = []


def fetchKantoPokemon():
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=151")
    allpokemon = response.json()
    
    for pokemon in allpokemon['results']:
        fetchPokemonData(pokemon)




def fetchPokemonData(pokemon):
    url = pokemon['url']
    response = requests.get(url)
    pokeData = response.json()
    pprint.pprint(pokeData['id'])
    
fetchKantoPokemon()

"""
red = Trainer.query.filter_by(name='gohan').first()
print(len(red.poke_belt))