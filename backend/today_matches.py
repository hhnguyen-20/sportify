import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from position import center
from api import API
from datetime import date
import pprint


def call_game_data():
    url = "https://api-nba-v1.p.rapidapi.com/games"
    today = str(date.today())
    today_querystring = {'date': today}
    live_querystring = {'live': 'all'}
    headers = {
        "X-RapidAPI-Key": API,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    today_response = requests.get(url, headers=headers, params=today_querystring)
    live_response = requests.get(url, headers=headers, params=live_querystring)
    return today_response.json(), live_response.json()


def format_live_game_data(live_response):
    '''
    { 'id': 13692,
      'league': 'standard',
      'season': 2023,
      'date': { 'start': '2024-04-09T23:00:00.000Z',
                'end': None,
                'duration': None},
      'stage': 2,
      'status': { 'clock': None,
                  'halftime': False,
                  'short': 3,
                  'long': 'Finished'},
      'periods': {'current': 4, 'total': 4, 'endOfPeriod': False},
      'arena': { 'name': 'Spectrum Center',
                 'city': 'Charlotte',
                 'state': 'NC',
                 'country': None},
      'teams': { 'visitors': { 'id': 8,
                               'name': 'Dallas Mavericks',
                               'nickname': 'Mavericks',
                               'code': 'DAL',
                               'logo': 'https://upload.wikimedia.org/wikipedia/fr/thumb/b/b8/Mavericks_de_Dallas_logo.svg/150px-Mavericks_de_Dallas_logo.svg.png'},
                 'home': { 'id': 5,
                           'name': 'Charlotte Hornets',
                           'nickname': 'Hornets',
                           'code': 'CHA',
                           'logo': 'https://upload.wikimedia.org/wikipedia/fr/thumb/f/f3/Hornets_de_Charlotte_logo.svg/1200px-Hornets_de_Charlotte_logo.svg.png'}},
      'scores': { 'visitors': { 'win': 0,
                                'loss': 0,
                                'series': {'win': 0, 'loss': 0},
                                'linescore': [ '36',
                                               '33',
                                               '28',
                                               '33'],
                                'points': 130},
                  'home': { 'win': 0,
                            'loss': 0,
                            'series': {'win': 0, 'loss': 0},
                            'linescore': ['18', '29', '36', '21'],
                            'points': 104}},
      'officials': [],
      'timesTied': None,
      'leadChanges': None,
      'nugget': None
    }
    '''
    live_match_count = live_response['results']
    formatted_live_matches = []
    if live_match_count == 0:
        print("There are no live matches currently.")
    for match in live_response['response']:
        formatted_data = [f"LIVE - Q{match['periods']['current']}-{match['status']['clock']}",
                          str(match['teams']['visitors']['name']),
                          match['scores']['visitors']['points'], 'vs.', match['scores']['home']['points'],
                          str(match['teams']['home']['name']), str(match['arena']['name']),
                          f"{str(match['arena']['city'])}, {str(match['arena']['state'])}"]
        formatted_live_matches.append(formatted_data)
    return formatted_live_matches


def format_today_game_data(today_response):
    today_match_count = today_response['results']
    formatted_today_matches = []
    if today_match_count == 0:
        print("There are no matches going on today")
    for match in today_response['response']:
        if match['status']['long'] == 'In Play':
            continue
        formatted_data = [str(date.today()), str(match['teams']['visitors']['name']),
                          match['scores']['visitors']['points'], 'vs.', match['scores']['home']['points'],
                          str(match['teams']['home']['name']), str(match['arena']['name']),
                          f"{str(match['arena']['city'])}, {str(match['arena']['state'])}"]
        formatted_today_matches.append(formatted_data)
    return formatted_today_matches


def main():
    today_games_json, live_games_json = call_game_data()
    live_matches = format_live_game_data(live_games_json)
    today_matches = format_today_game_data(today_games_json)
    # pprint.pprint(live_games_json)
    # pprint.pprint(today_games_json)
    # print(len(live_matches), len(today_matches))
    # pprint.pprint(live_matches, indent=2)
    # pprint.pprint(today_matches, indent=2)


if __name__ == '__main__':
    main()
