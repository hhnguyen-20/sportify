import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from position import center
from api import API


def call_live_game_data():
    url = "https://api-nba-v1.p.rapidapi.com/games"
    querystring = {'live': 'all'}
    headers = {
        "X-RapidAPI-Key": API,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def format_data(response):
    if response['results'] == 0:
        print("There are no live matches currently.")
    else:
        print(response)


def display_data(gameList):
    pass


def main():
    live_games_json = call_live_game_data()
    format_data(live_games_json)


main()