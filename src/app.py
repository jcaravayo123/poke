from flask import Flask, render_template, request
import requests
import sqlite3

app = Flask(__name__)

# Function to create SQLite database and table
def create_database():
    conn = sqlite3.connect('pokemon_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pokemon_data
                 (id INTEGER PRIMARY KEY, name TEXT, height INTEGER, weight INTEGER)''')
    conn.commit()
    conn.close()

# Function to insert data into SQLite database
def insert_into_database(name, height, weight):
    conn = sqlite3.connect('pokemon_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO pokemon_data (name, height, weight) VALUES (?, ?, ?)", (name, height, weight))
    conn.commit()
    conn.close()

# Function to fetch list of Pokémon names and URLs from PokeAPI
def fetch_pokemon_list():
    url = 'https://pokeapi.co/api/v2/pokemon/'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Extracting names and URLs of Pokémon
        pokemon_list = [(pokemon['name'].capitalize(), pokemon['url']) for pokemon in data['results']]
        return pokemon_list
    else:
        print("Failed to fetch Pokémon list from API")
        return []

# Route to render webpage
@app.route('/', methods=['GET', 'POST'])
def index():
    # Create database and table
    create_database()
    
    # Fetch list of Pokémon names and URLs
    pokemon_list = fetch_pokemon_list()
    
    # Initialize selected Pokémon data as None
    selected_pokemon_data = None
    
    # If form is submitted and a Pokémon is selected
    if request.method == 'POST' and 'pokemon' in request.form:
        selected_pokemon_url = request.form['pokemon']
        print("Selected Pokemon URL:", selected_pokemon_url)  # Debug print
        # Fetch data for the selected Pokémon
        selected_pokemon_data = fetch_pokemon_data(selected_pokemon_url)
        print("Selected Pokemon Data:", selected_pokemon_data)  # Debug print
        # Insert the selected Pokémon data into the database
        if selected_pokemon_data:
            insert_into_database(selected_pokemon_data['name'], selected_pokemon_data['height'], selected_pokemon_data['weight'])
    
    return render_template('index.html', pokemon_list=pokemon_list, selected_pokemon_data=selected_pokemon_data)

# Function to fetch data for a selected Pokémon
def fetch_pokemon_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch Pokémon data from API")
        return None

if __name__ == '__main__':
    app.run(debug=True)