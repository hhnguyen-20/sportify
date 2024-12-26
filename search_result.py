import tkinter as tk
from tkinter import ttk, messagebox
from urllib.request import urlopen
import PIL
from PIL import Image, ImageTk
from position import center
from api_functions import call_game_data, call_player_data
import time
from urllib.error import HTTPError

favorite_teams = []  # Global list to store favorite teams


def create_table(parent, title, columns):
    """
    Helper method to create tables for the team's data
    :param parent: The parent frame
    :param title: The title of the table
    :param columns: The tuple of columns of table
    :return: Tk Table
    """
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
    """
    Helper method that displays team data
    :param season_combobox: The combobox in Tk
    :param team_info: Team information
    :param frame_game: The frame that display game information about a certain team
    :param frame_player: The frame that display player information about a certain team
    :return: None
    """
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
    for g in game_data['response'][-10::]:
        game_tree.insert("", "end", values=(
            g['date']['start'][:10] if g['date']['start'] else "-",
            g['teams']['visitors']['name'] if g['teams']['visitors']['name'] else "-",
            f"{g['scores']['visitors']['points']} - {g['scores']['home']['points']}",
            g['teams']['home']['name'] if g['teams']['home']['name'] else "-",
            f"{g['arena']['name']}, {g['arena']['city']}, {g['arena']['state']}"
        ))

    # time.sleep(5)  # add a sleep here to avoid the rate limit

    # Player information table with title
    player_columns = ('name', 'jersey', 'position', 'height (m)', 'weight (kg)')
    player_tree = create_table(
        frame_player, "Team Players", player_columns
    )
    for p in player_data['response'][:]:
        player_tree.insert("", "end", values=(
            f"{p['firstname']} {p['lastname']}",
            p['leagues']['standard']['jersey'] if p['leagues']['standard']['jersey'] else "-",
            p['leagues']['standard']['pos'] if p['leagues']['standard']['pos'] else "-",
            p['height']['meters'] if p['height']['meters'] else "-",
            p['weight']['kilograms'] if p['weight']['kilograms'] else "-",
        ))


def add_to_favorites(team_code, team_name, team_logo, current_date):
    """
    Adds certain team into the Favorites Team list
    :param team_code: The team code
    :param team_name: The name of the team
    :param team_logo: The url of the logo of the team
    :param current_date: Added date
    :return: None
    """
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
    try:
        request = urlopen(url)
    except HTTPError:
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png"
        request = urlopen(url)

    image = Image.open(request)

    raw = image.resize((120, 120), PIL.Image.Resampling.LANCZOS)
    final_image = ImageTk.PhotoImage(raw)

    logo = tk.Label(window, image=final_image)
    logo.image = final_image
    logo.pack()


def display_data(root, team):
    """
    Displays searched team's data
    :param root: The main app window
    :param team: The searched team
    :return: None
    """
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

    fav_button = tk.Button(frame_team,
                           text="⭐ Add to Favorites",
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
