import threading
import tkinter as tk
from tkinter import messagebox
from search_result import display_data
from position import center
from show_fav import show_favorites
from today_matches import call_game_data, format_today_game_data, format_live_game_data
from league_standings import call_standings, format_data
from tkinter import ttk
from PIL import Image, ImageTk
from api_functions import call_team_data


def search():
    team_code = search_entry.get().strip().upper()  # Assuming the team code is entered and should be uppercase
    if team_code:  # Check if the entry is not empty
        # Run the API call and data display in a separate thread to avoid freezing the GUI
        threading.Thread(target=lambda: display_data(root, call_team_data(team_code))).start()
    elif team_code == "Enter a team name...":
        messagebox.showerror("showerror", "Error") 
    else:
        messagebox.showerror("showerror", "Error") 


def show():
    threading.Thread(target=lambda: show_favorites(root)).start()
    

# Create a Tkinter window
root = tk.Tk()
root.title("Home")

# center the root
center(root)

"""Frame 1"""
frame_1 = tk.Frame(root)
frame_1.pack()

home_photo = ImageTk.PhotoImage(Image.open("home_logo.png").resize((50, 50)))
home_logo = tk.Label(frame_1, image=home_photo)
home_logo.image = home_photo
home_logo.grid(row=0, column=0)

search_entry = tk.Entry(frame_1, width=50, fg="gray", bd=1, relief="solid")
search_entry.insert(0, "Enter a team name...")
search_entry.bind("<FocusIn>", lambda event: search_entry.delete(0, "end"))
search_entry.grid(row=0, column=1)

search_button = tk.Button(frame_1, text="Search", command=search)
search_button.grid(row=0, column=2)

fav_button = tk.Button(frame_1, text="Favorite Team", command=show)
fav_button.grid(row=0, column=3)

tk.Label(root, text="").pack()  # empty space

"""Frame 2"""
today_json, live_json = call_game_data()
live_games = format_live_game_data(live_json)
today_games = format_today_game_data(today_json)
frame_2 = tk.Frame(root, bd=1, relief="solid")
frame_2.pack()
row = 0
for text in live_games+today_games:
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

"""Frame 3"""
frame_3 = tk.Frame(root, bd=1, relief="solid")
frame_3.pack()

def show_east():
    pass

def show_west():
    pass

# Displaying League Standing in frame 3
east_standings, west_standings = call_standings()
east_formatted = format_data(east_standings)
west_formatted = format_data(west_standings)
button_frame = tk.Frame(frame_3)
east_button = tk.Button(button_frame, text='EAST', command=show_east)
east_button.grid(column=0, row=0)
separator = ttk.Separator(button_frame, orient='vertical')
separator.grid(column=1, row=0, sticky='ns')
west_button = tk.Button(button_frame, text='WEST', command=show_west)
west_button.grid(column=2, row=0)
# league_standing = tk.Label(frame_3, text="League Standing", width=70, height=20)
# league_standing.pack()
button_frame.pack()
frame_3.pack()
# Run the Tkinter event loop
root.mainloop()
