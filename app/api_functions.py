from api import API
import requests

headers = {
        "X-RapidAPI-Key": API,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }


def call_team_name(conference):
    """
    Calls API data to get teams based on conference
    :param conference: The desired conference
    :return: The API response in json format
    """
    querystring = {"league":"standard", "conference": conference}
    response = requests.get("https://api-nba-v1.p.rapidapi.com/teams", headers=headers, params=querystring)
    return response.json()


def call_team_data(team_id):
    """
    Calls API data to get team data based on team id
    :param team_id: A particular team id
    :return: The API response in json format
    """
    querystring = {"id": team_id}
    response = requests.get("https://api-nba-v1.p.rapidapi.com/teams", headers=headers, params=querystring)
    return response.json()


def call_game_data(team_id, season):
    """
    Calls the API data to get games based on team id and season
    :param team_id: A particular team id
    :param season: A desired season
    :return:  The API response in json format
    """
    querystring = {"team": str(team_id), "season": str(season)}
    response = requests.get("https://api-nba-v1.p.rapidapi.com/games", headers=headers, params=querystring)
    return response.json()


def call_player_data(team_id, season):
    """
    Calls the API data to get player data based on team id and season
    :param team_id: A particular team id
    :param season: A desired season
    :return: The API response in json format
    """
    querystring = {"team": str(team_id), "season": str(season)}
    response = requests.get("https://api-nba-v1.p.rapidapi.com/players", headers=headers, params=querystring)
    return response.json()