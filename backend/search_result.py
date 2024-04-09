import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request as req
from PIL import Image, ImageTk
import requests
from position import center
from api import API

favorite_teams = []  # Global list to store favorite teams

"""
Function to call the API data
"""
def call_api_data(url, team_id, season):
    querystring = {"team": str(team_id), "season": str(season)}
    headers = {
        "X-RapidAPI-Key": API,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

"""
Function to update the game and player based on the selected season
"""
def update_info(season_combobox, team_info, frame_game, frame_player):
    season_selected = season_combobox.get()
    game_data = call_api_data("https://api-nba-v1.p.rapidapi.com/games", team_info['id'], season_selected)
    player_data = call_api_data("https://api-nba-v1.p.rapidapi.com/players", team_info['id'], season_selected)
    
    # Update game info
    formatted_game_info = "\n".join(
        f"{g['teams']['home']['name']} vs. {g['teams']['visitors']['name']}, "
        f"Score: {g['scores']['home']['points']} - {g['scores']['visitors']['points']}, "
        f"Date: {g['date']['start'][:10]}, Arena: {g['arena']['city']}"
        for g in game_data['response'][:5]
    )
    for widget in frame_game.winfo_children():
        widget.destroy()

    # Displaying the formatted information
    game_title = tk.Label(frame_game, text="GAMES")
    game_title.grid(row=0, column=0, sticky="w")
    formatted_game_info_label = tk.Label(frame_game, text=formatted_game_info, justify=tk.LEFT)
    formatted_game_info_label.grid(row=1, column=0, sticky="w")
    
    # Update player info
    formatted_player_info = "\n".join(
        f"{p['firstname']} {p['lastname']}, Jersey: {p['leagues']['standard']['jersey']}, "
        f"Position: {p['leagues']['standard']['pos']}, Height: {p['height']['meters']} m, "
        f"Weight: {p['weight']['kilograms']} kg"
        for p in player_data['response'][:5]
    )
    for widget in frame_player.winfo_children():
        widget.destroy()

    # Displaying the formatted information
    player_title = tk.Label(frame_player, text="PLAYERS")
    player_title.grid(row=0, column=0, sticky="w")
    formatted_player_info_label = tk.Label(frame_player, text=formatted_player_info, justify=tk.LEFT)
    formatted_player_info_label.grid(row=1, column=0, sticky="w")

def add_to_favorites(team_id, team_name):
    if team_id not in favorite_teams:
        favorite_teams.append(team_name)
        messagebox.showinfo("Success", f"{team_name} added to favorites!")
    else:
        messagebox.showinfo("Info", f"{team_name} is already in your favorites.")

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
    req.urlretrieve(team_info['logo'], "logo.png")
    photo = ImageTk.PhotoImage(Image.open("logo.png").resize((50, 50)))
    
    # Display the image in the window
    logo = tk.Label(search_window, image=photo)
    logo.image = photo
    logo.pack()

    """Frame team"""
    frame_team = tk.Frame(search_window, bd=1, relief="solid")
    frame_team.pack(side="top", fill="x", padx=90, pady=10)

    team_title = tk.Label(frame_team, text="TEAM")
    team_title.grid(row=0, column=0, sticky="w")

    fav_button = tk.Button(frame_team, text="⭐️", command=lambda: add_to_favorites(team_info['id'], team_info['name']))
    fav_button.grid(row=0, column=1)

    # Formatting the information to be displayed
    formatted_team_info = f"Name: {team_info['name']}\n" \
                          f"Nickname: {team_info['nickname']}\n" \
                          f"City: {team_info['city']}\n" \
                          f"Conference: {team_info['leagues']['standard']['conference']}\n" \
                          f"Division: {team_info['leagues']['standard']['division']}\n" \
                          f"NBA Franchise: {'Yes' if team_info['nbaFranchise'] else 'No'}\n"

    # Displaying the formatted information
    formatted_team_info_label = tk.Label(frame_team, text=formatted_team_info, justify=tk.LEFT)
    formatted_team_info_label.grid(row=1, column=0, sticky="w", columnspan=2)

    """Season"""
    frame_season = tk.Frame(search_window)
    frame_season.pack(pady=10)

    seasons = ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015']

    season_title = tk.Label(frame_season, text="Select a season:")
    season_title.grid(row=0, column=0)
    season_combobox = ttk.Combobox(frame_season, values=seasons, state="readonly", width=10)
    season_combobox.grid(row=0, column=1)
    season_combobox.current(0)

    """Frame game"""
    frame_game = tk.Frame(search_window, bd=1, relief="solid")
    frame_game.pack(side="top", fill="x", padx=90, pady=10)

    """Frame player"""
    frame_player = tk.Frame(search_window, bd=1, relief="solid")
    frame_player.pack(side="top", fill="x", padx=90, pady=10)

    # Initial display
    update_info(season_combobox, team_info, frame_game, frame_player)

    # Bind the combobox selection event
    season_combobox.bind("<<ComboboxSelected>>", lambda event: update_info(season_combobox, team_info, frame_game, frame_player))
