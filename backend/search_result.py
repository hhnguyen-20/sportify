import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from position import center
from api import API


def call_game_data(team_id, season):
    url = "https://api-nba-v1.p.rapidapi.com/games"
    querystring = {"team": str(team_id), "season": str(season)}
    headers = {
        "X-RapidAPI-Key": API,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def call_player_data(team_id, season):
    url = "https://api-nba-v1.p.rapidapi.com/players"
    querystring = {"team": str(team_id), "season": str(season)}
    headers = {
        "X-RapidAPI-Key": API,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def display_data(root, team):
    search_window = tk.Toplevel(root)
    search_window.title("Team Data")
    center(search_window)

    """
    {'get': 'teams/',
    'parameters': {'code': 'ATL'},
    'errors': [], 
    'results': 1, 
    'response': [{
        'id': 1, 
        'name': 'Atlanta Hawks', 
        'nickname': 'Hawks', 
        'code': 'ATL', 
        'city': 'Atlanta', 
        'logo': 'https://upload.wikimedia.org/wikipedia/fr/e/ee/Hawks_2016.png', 
        'allStar': False, 
        'nbaFranchise': True, 
        'leagues': {
            'standard': {'conference': 'East', 'division': 'Southeast'}, 
            'vegas': {'conference': 'summer', 'division': None}, 
            'utah': {'conference': 'East', 'division': 'Southeast'}, 
            'sacramento': {'conference': 'East', 'division': 'Southeast'}
            }
        }]
    }
    """

    team_info = team['response'][0]

    """Logo"""
    # Load the image from the URL
    response = requests.get(team_info['logo'])
    image = Image.open(BytesIO(response.content))
    photo = ImageTk.PhotoImage(image.resize((50, 50)))

    # Display the image in the window
    logo = tk.Label(search_window, image=photo)
    logo.image = photo
    logo.pack()

    """Frame team"""
    frame_team = tk.Frame(search_window, bd=1, relief="solid")
    frame_team.pack(side="top", fill="x", padx=90, pady=10)

    team_title = tk.Label(frame_team, text="TEAM")
    team_title.grid(row=0, column=0, sticky="w")

    # Formatting the information to be displayed
    formatted_team_info = f"Name: {team_info['name']}\n" \
                          f"Nickname: {team_info['nickname']}\n" \
                          f"City: {team_info['city']}\n" \
                          f"Conference: {team_info['leagues']['standard']['conference']}\n" \
                          f"Division: {team_info['leagues']['standard']['division']}\n" \
                          f"NBA Franchise: {'Yes' if team_info['nbaFranchise'] else 'No'}\n"

    # Displaying the formatted information
    formatted_team_info_label = tk.Label(frame_team, text=formatted_team_info, justify=tk.LEFT)
    formatted_team_info_label.grid(row=1, column=0, sticky="w")

    """Season"""
    seasons = ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015']

    frame_season = tk.Frame(search_window)
    frame_season.pack(pady=10)

    season_title = tk.Label(frame_season, text="Select a season:")
    season_title.grid(row=0, column=0)
    season_combobox = ttk.Combobox(frame_season, values=seasons, state="readonly", width=10)
    season_combobox.grid(row=0, column=1)
    season_combobox.current(0)

    season_selected = season_combobox.get()

    """Frame game"""
    frame_game = tk.Frame(search_window, bd=1, relief="solid")
    frame_game.pack(side="top", fill="x", padx=90, pady=10)

    game_title = tk.Label(frame_game, text="GAMES")
    game_title.grid(row=0, column=0, sticky="w")

    game = call_game_data(team_info['id'], season_selected)
    formatted_game_info = ""
    for game_info in game['response'][:5]:
        formatted_game_info += f"{game_info['teams']['home']['name']} vs. {game_info['teams']['visitors']['name']}, " \
                              f"Score: {game_info['scores']['home']['points']} - {game_info['scores']['visitors']['points']}, " \
                              f"Date: {game_info['date']['start'][:10]}, " \
                              f"Arena: {game_info['arena']['city']}\n"

    # Displaying the formatted information
    formatted_game_info_label = tk.Label(frame_game, text=formatted_game_info, justify=tk.LEFT)
    formatted_game_info_label.grid(row=1, column=0, sticky="w")

    """Frame player"""
    frame_player = tk.Frame(search_window, bd=1, relief="solid")
    frame_player.pack(side="top", fill="x", padx=90, pady=10)

    player_title = tk.Label(frame_player, text="PLAYERS")
    player_title.grid(row=0, column=0, sticky="w")

    player = call_player_data(team_info['id'], season_selected)
    formatted_player_info = ""
    for player_info in player['response'][:5]:
        formatted_player_info += f"{player_info['firstname']} {player_info['lastname']}, " \
                                 f"Jersey: {player_info['leagues']['standard']['jersey']}, " \
                                 f"Position: {player_info['leagues']['standard']['pos']}, " \
                                 f"Height: {player_info['height']['meters']} m, " \
                                 f"Weight: {player_info['weight']['kilograms']} kg\n"

    # Displaying the formatted information
    formatted_player_info_label = tk.Label(frame_player, text=formatted_player_info, justify=tk.LEFT)
    formatted_player_info_label.grid(row=1, column=0, sticky="w")
