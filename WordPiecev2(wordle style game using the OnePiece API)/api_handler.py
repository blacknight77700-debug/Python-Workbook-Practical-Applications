"""Dedicated to communicating with the One Piece API, downloading the character list, 
and saving/loading it locally as a JSON cache file so it doesn't overwhelm the API on every single test run."""

# Imports

import requests
import json
import os
import re


api_url = "https://onepieceapi.com/api/characters"

# Rule

def normalize_value(x):
    """Normalizes raw input values by stripping whitespace, 
    handling strings, numbers, and standardizing null equivalents."""

    if x is None:
        return None


    if isinstance(x, (int, float)):
        return x


    if isinstance(x, str):
        x = re.sub(r'\s+', ' ',x).strip()


        if x.lower() in ['none', 'null', 'n/a', 'na', '']:
            return None
        return x.lower()
       
    return x


class WordPieceManager:
    """A manager class to handle fetching, caching, and loading One Piece
    character data from an external API or local storage"""

    @staticmethod
    def fetch_all_raw_characters(api_url):
        """Fetches all raw character records from a paginated API endpoint.

        Continuously queries the target API using page and limit query parameters 
        until all available records are retrieved."""

        all_results = []
        page = 1
        limit = 100

        while True:

            try:
                response = requests.get(api_url, params={"page": page, "limit": limit})

                if response.status_code != 200:
                    print(f"Error on page {page}: {response.status_code}")
                    break

                data = response.json()
                results = (data.get("results", data) if isinstance(data,dict) else data)

                if not results:
                    break

                all_results.extend(results)

                if len(results) < limit:
                    break

                page += 1

            except requests.exceptions.RequestException as e:
                print(f"An error has occurred {e}")
                break


        return all_results

    @staticmethod
    def fetch_character_name_list(api_url="https://onepieceapi.com/api/characters"):
        """Extracts a flat list of English character names from the API data source.

        Utilizes the paginated raw fetcher to gather all characters and filters 
        out records with missing or invalid names for autocomplete use."""

        menu_names = []
        results = WordPieceManager.fetch_all_raw_characters(api_url)

        for character in results:
       
            name_field = character.get('name')

            if isinstance(name_field, dict):
                        name = name_field.get('en')
            else:
                name = name_field

            if not name:
                print(f"Skipping incomplete record: {character}")
                continue

            menu_names.append(name)


        return menu_names
        
    @staticmethod
    def fetch_character_list(api_url="https://onepieceapi.com/api/characters"):
        """Sends a paginated request to the API, parses responses, and extracts 
        targeted character attributes into a normalized list of dictionaries."""

        print("Fetching data from OnePieceAPI")

        all_characters = []

        results = WordPieceManager.fetch_all_raw_characters(api_url)
        for character in results:

            name_dict = character.get('name',{})
            name = name_dict.get('en') if isinstance(name_dict, dict) else name_dict
            
            if not name:
                print(f"Skipping incomplete record: {character}")
                continue

            extra = character.get('extra_data') or {}

            raw_bounty = character.get('bounties',[])

            active_bounty = next(
                (
                    bounty['amount']
                    for bounty in raw_bounty
                    if bounty.get('is_active')
                )
            )   

            character_info = {
                'name': name,
                'age': character.get('age'),
                'height': character.get('height'),
                'affiliation': extra.get('affiliation'),
                'first_appearance': extra.get('first_appearance'),
                'bounties': active_bounty,
                'devil-fruits': character.get('devil-fruits')
            }

            for key in character_info:
                character_info[key] = normalize_value(character_info[key])

            all_characters.append(character_info)

    
        return all_characters
    
    @staticmethod
    def dump_cache(all_characters, filename='wordpiece_characters.json'):
        """Saves a processed character data list into a local JSON file  
        that is formatted with readable indentation"""

        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(all_characters, file, indent=4)
                print(f"Successfully saved data to {filename}")

        except Exception as e:
            print(f"An error has occurred: {e} ")

    @staticmethod     
    def cache_manager(api_url="https://onepieceapi.com/api/characters?limit=7000",filename='wordpiece_characters.json'):
        """Controls loading character data by checking for a local cache file
          first, falling back to an API fetch if the file is missing or corrupted"""
        
        if os.path.exists(filename):
            print("loading character data from local cache")

            try:

                with open(filename,'r', encoding='utf-8') as file:
                    return json.load(file)
                
            except json.JSONDecodeError:
                print("Cache file is corrupted. Falling back to API...")
                pass


        print(f"No local cache found. Fetching fresh data from API...")
        all_characters = WordPieceManager.fetch_character_list(api_url)
        WordPieceManager.dump_cache(all_characters)

        return all_characters