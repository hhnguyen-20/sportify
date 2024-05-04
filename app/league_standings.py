import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from position import center
from api import API
import pprint


def call_standings():
    url = "https://api-nba-v1.p.rapidapi.com/standings"
    east_querystring = {'league': 'standard', 'season': '2023', 'conference': 'east'}
    west_querystring = {'league': 'standard', 'season': '2023', 'conference': 'west'}
    headers = {
        "X-RapidAPI-Key": API,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    east_conf = requests.get(url, headers=headers, params=east_querystring)
    west_conf = requests.get(url, headers=headers, params=west_querystring)
    return east_conf.json(), west_conf.json()


def format_data(conf_json):
    '''
    {'conference': {'loss': 17, 'name': 'east', 'rank': 1, 'win': 62},
     'division': {'gamesBehind': None,
                    'loss': 17,
                    'name': 'atlantic',
                    'rank': 1,
                    'win': 62},
     'gamesBehind': None,
     'league': 'standard',
     'loss': {'away': 14,
                'home': 3,
                'lastTen': 3,
                'percentage': '0.215',
                'total': 17},
     'season': 2023,
     'streak': 1,
     'team': {'code': 'BOS',
                'id': 2,
                'logo': 'https://upload.wikimedia.org/wikipedia/fr/thumb/6/65/Celtics_de_Boston_logo.svg/1024px-Celtics_de_Boston_logo.svg.png',
                'name': 'Boston Celtics',
                'nickname': 'Celtics'},
     'tieBreakerPoints': None,
     'win': {'away': 27,
               'home': 35,
               'lastTen': 7,
               'percentage': '0.785',
               'total': 62},
     'winStreak': False}
    '''
    team_standing_dict = {}
    for team in conf_json['response']:
        last_10_stat = f"{team['win']['lastTen']}-{team['loss']['lastTen']}"
        home_stat = f"{team['win']['home']}-{team['loss']['home']}"
        away_stat = f"{team['win']['away']}-{team['loss']['away']}"
        if not team['winStreak']:
            streak = f"L{team['streak']}"
        else:
            streak = f"W{team['streak']}"
        if team['gamesBehind'] is None:
            games_behind = "-"
        else:
            games_behind = team['gamesBehind']
        team_standing_dict[team['conference']['rank']] = [team['team']['logo'], team['team']['nickname'],
                                                          team['conference']['win'],
                                                          team['conference']['loss'], team['win']['percentage'],
                                                          games_behind, home_stat, away_stat, last_10_stat, streak]
    return team_standing_dict


def main():
    east_conf_data, west_conf_data = call_standings()
    east_standing_dict = format_data(east_conf_data)
    west_standing_dict = format_data(west_conf_data)
    print("East Conference")
    pprint.pprint(east_standing_dict)
    print("------------------------------------------------------------")
    print("West Conference")
    pprint.pprint(west_standing_dict)


if __name__ == '__main__':
    main()
