import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from position import center
from api import API
from datetime import date
import pprint


def call_live_game_data():
    url = "https://api-nba-v1.p.rapidapi.com/games"
    today = str(date.today())
    querystring = {'date': today}
    headers = {
        "X-RapidAPI-Key": API,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def format_data(response):
    """
    {   'id': 13650,
        'league': 'standard',
        'season': 2023,
        'date': {'start': '2024-04-03T23:00:00.000Z', 'end': None, 'duration': None},
        'stage': 2,
        'status': {'clock': '7:43', 'halftime': False, 'short': 2, 'long': 'In Play'},
        'periods': {'current': 1, 'total': 4, 'endOfPeriod': False},
        'arena': {'name': 'Spectrum Center', 'city': 'Charlotte', 'state': 'NC', 'country': None},
        'teams':
            {'visitors':
                {'id': 29, 'name': 'Portland Trail Blazers', 'nickname': 'Trail Blazers', 'code': 'POR',
                 'logo': 'https://upload.wikimedia.org/wikipedia/en/thumb/2/21/Portland_Trail_Blazers_logo.svg / 1200px - Portland_Trail_Blazers_logo.svg.png'},
             'home':
                {'id': 5, 'name': 'Charlotte Hornets', 'nickname': 'Hornets', 'code': 'CHA',
                 'logo': 'https://upload.wikimedia.org/wikipedia/fr/thumb/f/f3/Hornets_de_Charlotte_logo.svg / 1200px - Hornets_de_Charlotte_logo.svg.png'}
            },
        'scores':
            {'visitors':
                {'win': 0, 'loss': 0, 'series': {'win': 0, 'loss': 0}, 'linescore': ['7', '', '', ''],'points': 7},
             'home':
                {'win': 0, 'loss': 0, 'series': {'win': 0, 'loss': 0}, 'linescore': ['9', '', '', ''],'points': 11}
            },
        'officials': [],
        'timesTied': None,
        'leadChanges': None,
        'nugget': None
    }
    """
    live_match_count = response['results']
    formatted_live_matches = []
    if live_match_count == 0:
        print("There are no live matches currently.")
    for match in response['response']:
        formatted_string = f"Q{match['periods']['current']}   {match['status']['clock']}      {match['teams']['visitors']['name']}   {match['scores']['visitors']['points']}     vs.     {match['scores']['home']['points']}   {match['teams']['home']['name']}      {match['arena']['name']}      {match['arena']['city']}, {match['arena']['state']}"
        formatted_live_matches.append(formatted_string)
    return formatted_live_matches

def display_data(gameList):
    pass


def main():
    live_games_json = call_live_game_data()
    pprint.pp(live_games_json, indent=2)
    # match_strings = format_data(live_games_json)
    # for match_str in match_strings:
    #     print(match_str)


if __name__ == '__main__':
    main()
