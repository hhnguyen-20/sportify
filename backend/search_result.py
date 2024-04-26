import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from position import center
import io
from api_functions import call_game_data, call_player_data
import time

favorite_teams = []  # Global list to store favorite teams


def create_table(parent, title, columns):
    frame = tk.Frame(parent, bd=1, relief="solid")
    frame.pack(side="top", fill="x", padx=10, pady=5)

    title_label = tk.Label(frame, text=title, font=('Arial', 12, 'bold'))
    title_label.pack(side="top", fill="x")

    table = ttk.Treeview(frame, columns=columns, show="headings", height=5)
    for col in columns:
        table.heading(col, text=col.title())
        table.column(col, anchor="center", width=80)
    table.pack(expand=True, fill='both')
    return table


def update_info(season_combobox, team_info, frame_game, frame_player):
    # Retrieve data
    season_selected = season_combobox.get()
    game_data = call_game_data(team_info['id'], season_selected)
    player_data = call_player_data(team_info['id'], season_selected)

    # Clear existing widgets
    for widget in frame_game.winfo_children() + frame_player.winfo_children():
        widget.destroy()

    # Game information table with title
    game_columns = ('date', 'visitors', 'score', 'home', 'arena')
    game_tree = create_table(
        frame_game, "Recent Games", game_columns
    )
    for g in game_data['response'][:10]:
        game_tree.insert("", "end", values=(
            g['date']['start'][:10],
            g['teams']['visitors']['name'],
            f"{g['scores']['visitors']['points']} - {g['scores']['home']['points']}",
            g['teams']['home']['name'],
            f"{g['arena']['name']}, {g['arena']['city']}, {g['arena']['state']}"
        ))

    time.sleep(5)  # add a sleep here to avoid the rate limit

    # Player information table with title
    player_columns = ('name', 'jersey', 'position', 'height (m)', 'weight (kg)')
    player_tree = create_table(
        frame_player, "Team Players", player_columns
    )
    for p in player_data['response'][:10]:
        player_tree.insert("", "end", values=(
            f"{p['firstname']} {p['lastname']}",
            p['leagues']['standard']['jersey'],
            p['leagues']['standard']['pos'],
            p['height']['meters'],
            p['weight']['kilograms']
        ))


def add_to_favorites(team_code, team_name, team_logo, current_date):
    roll_number = len(favorite_teams) + 1
    if team_code not in [team[1] for team in favorite_teams]:
        favorite_teams.append((roll_number, team_code, team_name, team_logo, current_date))
        messagebox.showinfo("Success", f"{team_name} added to favorites!")
    else:
        messagebox.showinfo("Info", f"{team_name} is already in your favorites.")



def display_team_logo(window, url):
    """
    Display the team logo in the window
    """
    response = requests.get(url)
    image_bytes = io.BytesIO(response.content)
    pil_image = Image.open(image_bytes)
    pil_image = pil_image.resize((120, 120))
    photo = ImageTk.PhotoImage(pil_image)

    logo = tk.Label(window, image=photo)
    logo.image = photo
    logo.pack()


def display_data(root, team):
    search_window = tk.Toplevel(root)
    search_window.title("Team Data")
    center(search_window)

    team_info = team['response'][0]

    """Logo"""
    display_team_logo(search_window, team_info['logo'])

    """Frame team"""
    frame_team = tk.Frame(search_window)
    frame_team.pack(side="top", fill="x", padx=90, pady=10)

    team_columns = ('Name', 'Nickname', 'City', 'Conference', 'Division', 'NBA Franchise')
    team_table = create_table(frame_team, "Team Information", team_columns)
    team_data = (
        team_info['name'],
        team_info['nickname'],
        team_info['city'],
        team_info['leagues']['standard']['conference'],
        team_info['leagues']['standard']['division'],
        "Yes" if team_info['nbaFranchise'] else "No"
    )
    team_table.insert("", "end", values=team_data)

    fav_button = tk.Button(frame_team, text="⭐️",
                           command=lambda: add_to_favorites(
                               team_info['code'],
                               team_info['name'],
                               team_info['logo'],
                               time.strftime("%m/%d/%Y %H:%M:%S")))
    fav_button.pack(side="top", padx=5, pady=5)

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
    frame_game = tk.Frame(search_window)
    frame_game.pack(side="top", fill="x", padx=90, pady=20)

    """Frame player"""
    frame_player = tk.Frame(search_window)
    frame_player.pack(side="top", fill="x", padx=90, pady=20)

    # Initial display
    update_info(season_combobox, team_info, frame_game, frame_player)

    # Bind the combobox selection event
    season_combobox.bind("<<ComboboxSelected>>",
                         lambda event: update_info(season_combobox, team_info, frame_game, frame_player))
