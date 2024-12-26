import threading
import tkinter as tk
from tkinter import messagebox
import PIL.Image
from search_result import display_data
from position import center
from show_fav import show_favorites
from today_matches import format_today_game_data, format_live_game_data
from league_standings import format_data
from tkinter import ttk
from PIL import Image, ImageTk
from urllib.request import urlopen
from api_functions import call_team_name, call_team_data, call_live_game_data, call_standings
from urllib.error import HTTPError

east_teams_data = call_team_name("east")
west_teams_data = call_team_name("west")
teams_data = {**east_teams_data, **west_teams_data}

team_names = {team['name']: team['id'] for team in teams_data.get('response')}


def search():
    """
    Helper method Gets the search word and starts a thread to call the team data on the search word
    :return: None
    """
    team_search = search_entry.get().strip()
    if team_search in team_names:
        team_id = team_names.get(team_search)
        threading.Thread(target=lambda: display_data(root, call_team_data(team_id))).start()
    else:
        messagebox.showerror("showerror", "Error: Invalid team name")


def show():
    """
    Helper method that creates a thread to show favorite teams tab
    :return: None
    """
    threading.Thread(target=lambda: show_favorites(root)).start()


def update_dropdown(event):
    """
    Helper method that updates the dropdown menu based on user input in the search bar
    :return: None
    """
    search_term = search_entry.get().lower()
    filtered_teams = [name for name in team_names.keys() if search_term in name.lower()]
    search_entry['values'] = filtered_teams
    search_entry.event_generate('<Down>')


# Create a Tkinter window for the app
root = tk.Tk()
root.title("Home")
center(root)  # Center the main window

"""Frame 1: App logo, Search bar, Search button, and Favorite Teams button"""
frame_1 = tk.Frame(root)
frame_1.pack()

# App logo
image_request = urlopen(
    "https://img.freepik.com/free-vector/hand-drawn-flat-design-basketball-logo_23-2149392459.jpg")
raw_image = Image.open(image_request)
resized_raw = raw_image.resize((50, 50), PIL.Image.Resampling.LANCZOS)
home_photo = ImageTk.PhotoImage(resized_raw)
home_logo = tk.Label(frame_1, image=home_photo)
home_logo.image = home_photo
home_logo.grid(row=0, column=0)

# Search bar
search_entry = ttk.Combobox(frame_1, values=list(team_names.keys()), width=50, foreground="gray")
search_entry.set("Enter a team name...")
search_entry.bind("<FocusIn>",
                  lambda event: search_entry.set('') if search_entry.get() == "Enter a team name..." else None)
search_entry.bind("<KeyRelease>", update_dropdown)
search_entry.grid(row=0, column=1)

# Search button
search_button = tk.Button(frame_1, text="Search", command=search)
search_button.grid(row=0, column=2)

# Favorite Teams button
fav_button = tk.Button(frame_1, text="Favorite Team", command=show)
fav_button.grid(row=0, column=3)

tk.Label(root, text="").pack()  # empty space

"""Frame 2: List of live games and today's games in UTC time format"""
today_json, live_json = call_live_game_data()
live_games = format_live_game_data(live_json)
today_games = format_today_game_data(today_json)
frame_2 = tk.Frame(root, bd=1, relief="solid")
frame_2.pack()
row = 0
for text in live_games + today_games:
    game_frame = tk.Frame(frame_2, bg='white', bd=1, relief='solid')
    if not text[0].find("LIVE"):
        time_label = tk.Label(game_frame, text=text[0], bg='white', fg='red', width=15, height=2)
    else:
        time_label = tk.Label(game_frame, text=text[0], bg='white', fg='black', width=15, height=2)
    away_team_label = tk.Label(game_frame, text=text[1], bg='white', fg='black', width=20, height=2)
    away_score_label = tk.Label(game_frame, text=text[2], bg='white', fg='black', width=5, height=2)
    vs_label = tk.Label(game_frame, text=text[3], bg='white', fg='black', height=2)
    home_score_label = tk.Label(game_frame, text=text[4], bg='white', fg='black', width=5, height=2)
    home_team_label = tk.Label(game_frame, text=text[5], bg='white', fg='black', width=20, height=2)
    arena_label = tk.Label(game_frame, text=text[6], bg='white', fg='black', width=20, height=2)
    city_state_label = tk.Label(game_frame, text=text[7], bg='white', fg='black', width=15, height=2)
    time_label.grid(row=row, column=0, pady=5)
    away_team_label.grid(row=row, column=1, pady=5)
    away_score_label.grid(row=row, column=2, pady=5)
    vs_label.grid(row=row, column=3, pady=5)
    home_score_label.grid(row=row, column=4, pady=5)
    home_team_label.grid(row=row, column=5, pady=5)
    arena_label.grid(row=row, column=6, pady=5)
    city_state_label.grid(row=row, column=7, pady=5)
    row += 1
    game_frame.pack()

tk.Label(root, text="").pack()  # empty space

"""Frame 3: East and West Conference Standing"""
frame_3 = tk.Frame(root)

east_standings, west_standings = call_standings()
east_formatted = format_data(east_standings)
west_formatted = format_data(west_standings)

east_frame = tk.Frame(frame_3, bg='white', bd=1, relief='solid')
west_frame = tk.Frame(frame_3, bg='white', bd=1, relief='solid')


def load_image(image_url):
    """
    Loads the image to be placed in the standings by taking in the url of the image
    :param image_url: The url for the image
    :return: Rendered image
    """
    try:
        request = urlopen(image_url)
    except HTTPError:
        image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png"
        request = urlopen(image_url)

    image = Image.open(request)

    raw = image.resize((35, 35), PIL.Image.Resampling.LANCZOS)
    final_image = ImageTk.PhotoImage(raw)

    return final_image


def standing_labels(conf_frame):
    """
    Creates header labels for each conference standing's tk frame
    :param conf_frame: The frame to put the header labels
    :return: None
    """
    team_header = tk.Label(conf_frame, text="Team", width=5, height=1, bg='white', fg='black')
    win_header = tk.Label(conf_frame, text="W", width=5, height=1, bg='white', fg='black')
    loss_header = tk.Label(conf_frame, text="L", width=5, height=1, bg='white', fg='black')
    pct_header = tk.Label(conf_frame, text="Pct", width=5, height=1, bg='white', fg='black')
    gb_header = tk.Label(conf_frame, text="GB", width=5, height=1, bg='white', fg='black')
    home_header = tk.Label(conf_frame, text="Home", width=5, height=1, bg='white', fg='black')
    away_header = tk.Label(conf_frame, text="Away", width=5, height=1, bg='white', fg='black')
    streak_header = tk.Label(conf_frame, text="Strk", width=5, height=1, bg='white', fg='black')
    header_row = 0
    team_header.grid(row=header_row, column=0, columnspan=3)
    win_header.grid(row=header_row, column=3)
    loss_header.grid(row=header_row, column=4)
    pct_header.grid(row=header_row, column=5)
    gb_header.grid(row=header_row, column=6)
    home_header.grid(row=header_row, column=7)
    away_header.grid(row=header_row, column=8)
    streak_header.grid(row=header_row, column=9)


def create_league_standing(conf_frame, formatted_conf):
    """
    Helper method that designs league standings for a given conference
    :param conf_frame: The conference TK frame
    :param formatted_conf: the formatted Conference data
    :return: None
    """
    standing_row = 1
    for rank, team in sorted(formatted_conf.items()):
        position = tk.Label(conf_frame, text=rank, width=5, height=1, bg='white', fg='black')
        team_logo = load_image(team[0])
        logo_label = tk.Label(conf_frame, bg='white', image=team_logo)
        logo_label.image = team_logo
        nickname_label = tk.Label(conf_frame, text=team[1], width=10, height=1, bg='white', fg='black')
        wins = tk.Label(conf_frame, text=team[2], width=5, height=1, bg='white', fg='black')
        losses = tk.Label(conf_frame, text=team[3], width=5, height=1, bg='white', fg='black')
        win_percent = tk.Label(conf_frame, text=team[4], width=5, height=1, bg='white', fg='black')
        games_behind = tk.Label(conf_frame, text=team[5], width=5, height=1, bg='white', fg='black')
        home_stat_label = tk.Label(conf_frame, text=team[6], width=5, height=1, bg='white', fg='black')
        away_stat_label = tk.Label(conf_frame, text=team[7], width=5, height=1, bg='white', fg='black')
        last_ten_stat_label = tk.Label(conf_frame, text=team[8], width=5, height=1, bg='white', fg='black')
        streak_label = tk.Label(conf_frame, text=team[9], width=5, height=1, bg='white', fg='black')
        position.grid(row=standing_row, column=0, pady=1)
        logo_label.grid(row=standing_row, column=1, pady=1)
        nickname_label.grid(row=standing_row, column=2, pady=1)
        wins.grid(row=standing_row, column=3, pady=1)
        losses.grid(row=standing_row, column=4, pady=1)
        win_percent.grid(row=standing_row, column=5, pady=1)
        games_behind.grid(row=standing_row, column=6, pady=1)
        home_stat_label.grid(row=standing_row, column=7, pady=1)
        away_stat_label.grid(row=standing_row, column=8, pady=1)
        last_ten_stat_label.grid(row=standing_row, column=9, pady=1)
        streak_label.grid(row=standing_row, column=9, pady=1)
        standing_row += 1


def show_east():
    """
    Creates the East conference standing
    :return: None
    """
    west_frame.pack_forget()
    standing_labels(east_frame)
    create_league_standing(east_frame, east_formatted)
    east_frame.pack()


def show_west():
    """
        Creates the West conference standing
        :return: None
        """
    east_frame.pack_forget()
    standing_labels(west_frame)
    create_league_standing(west_frame, west_formatted)
    west_frame.pack()


# Buttons for East and West Conferences
button_frame = tk.Frame(frame_3)
east_button = tk.Button(button_frame, text='EAST', command=show_east)
east_button.grid(column=0, row=0)
separator = ttk.Separator(button_frame, orient='vertical')
separator.grid(column=1, row=0, sticky='ns')
west_button = tk.Button(button_frame, text='WEST', command=show_west)
west_button.grid(column=2, row=0)

button_frame.pack()
frame_3.pack()
button_frame.mainloop()
frame_3.mainloop()

# Run the Tkinter event loop
root.mainloop()
