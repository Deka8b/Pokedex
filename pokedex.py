import time

import PIL.Image, PIL.ImageTk
import tkinter as tk
import urllib3
import requests

import pyttsx3
import pypokedex
from io import BytesIO
from opposite_types import opposite_types
import playsound


def SpeakText(text_variable):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text_variable)
    engine.runAndWait()


def get_pokemon_description(number):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{number}")
    description = response.json().get("flavor_text_entries")[1].get("flavor_text").replace("\n", " ").replace("", " ")
    return description


window = tk.Tk()

window.geometry("600x800")
window.title("Pokedex")
window.config(padx=10, pady=10)

title_label = tk.Label(window, text="Welcome to PokedexApp \n 898 Pokemons in Pokedex")
title_label.config(font=("Roboto", 32))
title_label.pack(padx=10, pady=10)

pokemon_image = tk.Label(window)
pokemon_image.pack(padx=10, pady=10)

pokemon_information = tk.Label(window)
pokemon_information.config(font=("Roboto", 20))
pokemon_information.pack(padx=10, pady=10)

pokemon_moves = tk.Label(window)
pokemon_information.config(font=("Roboto", 15))
pokemon_moves.pack(pady=10, padx=10)

pokemon_types = tk.Label(window)
pokemon_types.config(font=("Roboto", 15))
pokemon_types.pack(padx=10, pady=10)


def load_pokemon():
    pokemon = pypokedex.get(name=text_id_name.get(1.0, "end-1c"))
    http = urllib3.PoolManager()
    response = http.request("GET", pokemon.sprites.front["default"])
    image = PIL.Image.open(BytesIO(response.data))
    img = PIL.ImageTk.PhotoImage(image)
    pokemon_image.config(image=img)
    pokemon_image.image = img

    pokemon_information.config(text=f"{pokemon.dex} - {pokemon.name.capitalize()} \n "
                                    f"Atk: {pokemon.base_stats.attack}, Def: {pokemon.base_stats.defense}, Speed: {pokemon.base_stats.speed}")
    enemies = str([opposite_types[elem] for elem in pokemon.types]).replace("[", "").replace("]", "").replace("'", "")
    pokemon_types.config(text=f"Type: " + ', '.join(pokemon.types) + "\n Vulnerability: " + enemies)

    pkmn_moves = {move.level: move.name.replace("-", " ") for move in pokemon.moves["red-blue"] if move.level}
    sorted_moves = sorted(pkmn_moves)
    description = get_pokemon_description(pokemon.dex)
    moves_string = f"{description}\n\nAttacks: \n"
    for elem in sorted_moves:
        moves_string += f"Level: {elem}:  {pkmn_moves[elem]}\n"
    pokemon_moves.config(text=f"{moves_string}")

    SpeakText(f"Number: {pokemon.dex}, {pokemon.name}. Pokemon type: {', '.join(pokemon.types)}")
    time.sleep(0.5)
    playsound.playsound(fr'C:\Users\48530\PycharmProjects\Pokedex\pokemon_cries\{pokemon.name.capitalize()}.mp3', True)


label_id_name = tk.Label(window, text="Insert ID(1-898) or Name")
label_id_name.config(font=("Arial", 20))
label_id_name.pack(padx=10, pady=10)

text_id_name = tk.Text(window, height=1, background="azure")
text_id_name.config(font=("Arial", 20))
text_id_name.pack(pady=10, padx=10)

btn_load = tk.Button(window, text="Load Pokemon!", command=load_pokemon, background="chartreuse4")
btn_load.config(font=("Arial", 20))
btn_load.pack(padx=10, pady=10)

window.mainloop()
