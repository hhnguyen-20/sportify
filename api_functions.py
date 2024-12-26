import requests
from datetime import date

BASE_URL = "https://v2.nba.api-sports.io"
HEADERS = {
    'x-rapidapi-host': "v2.nba.api-sports.io",
    'x-rapidapi-key': "xxxxxxxxxxxxxxxxxxxxx"
}


def _request(endpoint: str, params: dict = None) -> dict:
    """
    Helper function to make a GET request to the NBA API-Sports endpoint.
    :param endpoint: The API endpoint (e.g., '/teams')
    :param params: Dictionary of query parameters
    :return: JSON response as a dictionary
    """
    if params is None:
        params = {}
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Log or handle error as needed
        print(f"Error fetching data from {url}: {e}")
        return {"response": [], "results": 0}


def call_team_name(conference: str) -> dict:
    """
    Fetches teams by conference.
    :param conference: 'east' or 'west'
    :return: JSON response dict
    """
    params = {
        "league": "standard",
        "conference": conference
    }
    return _request("/teams", params)


def call_team_data(team_id: int) -> dict:
    """
    Fetches data about a specific team based on the team_id.
    :param team_id: The team's unique ID
    :return: JSON response dict
    """
    params = {
        "id": team_id
    }
    return _request("/teams", params)


def call_game_data(team_id: int, season: str) -> dict:
    """
    Fetches game data for a specific team in a particular season.
    :param team_id: The team's unique ID
    :param season: The season, e.g., '2023'
    :return: JSON response dict
    """
    params = {
        "team": team_id,
        "season": season
    }
    return _request("/games", params)


def call_live_game_data() -> tuple[dict, dict]:
    """
    Fetches two sets of data:
    1. Today's games (by date).
    2. Currently live games.
    :return: A tuple: (today_data, live_data)
    """
    today_str = date.today().strftime("%m-%d-%Y")

    # Games on today's date
    today_data = _request("/games", {"date": today_str})

    # All live games
    live_data = _request("/games", {"live": "all"})

    return today_data, live_data


def call_player_data(team_id: int, season: str) -> dict:
    """
    Fetches player data for a specific team in a particular season.
    :param team_id: The team's unique ID
    :param season: The season, e.g., '2023'
    :return: JSON response dict
    """
    params = {
        "team": team_id,
        "season": season
    }
    return _request("/players", params)


def call_standings(season: str = "2023") -> tuple[dict, dict]:
    """
    Fetches standings for East and West conferences.
    :param season: Which season to fetch, defaults to '2023'
    :return: A tuple: (east_standings, west_standings)
    """
    # East
    east_data = _request("/standings", {
        "league": "standard",
        "season": season,
        "conference": "east"
    })

    # West
    west_data = _request("/standings", {
        "league": "standard",
        "season": season,
        "conference": "west"
    })

    return east_data, west_data
