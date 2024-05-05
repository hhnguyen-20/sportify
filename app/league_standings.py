import requests
from api import API
import pprint


def call_standings():
    """
    Calls API data to get the league standings
    :return: The API response for east conference and west conference standings in json format
    """
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
    """
    Formats the json response by extracting important information and putting them into a list
    :param conf_json: The conference json response
    :return: The list of formatted conference standing data
    """
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
