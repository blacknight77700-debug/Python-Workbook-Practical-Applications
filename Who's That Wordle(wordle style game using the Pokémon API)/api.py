"""Handles all communication with external APIs. Sends requests to PokéAPI to fetch Pokémon names.

Filters the list to only return 5-letter names."""

# Imports
import requests
import json

api_url = "https://pokeapi.co/api/v2/pokemon?limit=1300"


def fetch_pokemon_list(api_url):
    """Sends an HTTP request to the PokéAPI to pull a large raw list of 
    Pokémon names and identifiers."""

    all_pokemon = []

    print("Fetching data from PokeAPI...")

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()

            for gen in data['results']:
                all_pokemon.append(gen['name'])
                
        else:
            print(f"Error: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return all_pokemon


def filter_five_letter_words(all_pokemon):
    """Processes the raw list, filters out names that aren't exactly 5 letters long, removes any names 
    with special characters or hyphens, and returns a clean list of valid target words."""

    five_letter_pokemon = []

    for pokemon in all_pokemon:
        if len(pokemon) == 5:
            if pokemon.isalpha():
                five_letter_pokemon.append(pokemon)
            else:
                print(f"The pokemon contains spaces, hyphens, or numbers.")

    return five_letter_pokemon