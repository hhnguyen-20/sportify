from api import API
import requests

headers = {
        "X-RapidAPI-Key": API,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }


def call_team_name():
    response = requests.get("https://api-nba-v1.p.rapidapi.com/teams", headers=headers)
    return response.json()


def call_team_data(team_id):
    querystring = {"id": team_id}
    response = requests.get("https://api-nba-v1.p.rapidapi.com/teams", headers=headers, params=querystring)
    return response.json()


def call_game_data(team_id, season):
    querystring = {"team": str(team_id), "season": str(season)}
    response = requests.get("https://api-nba-v1.p.rapidapi.com/games", headers=headers, params=querystring)
    return response.json()


def call_player_data(team_id, season):
    querystring = {"team": str(team_id), "season": str(season)}
    response = requests.get("https://api-nba-v1.p.rapidapi.com/players", headers=headers, params=querystring)
    return response.json()