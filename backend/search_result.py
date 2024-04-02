import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from position import center


def display_data(root, team):
    search_window = tk.Toplevel(root)
    search_window.title("Team Data")
    center(search_window)

    # team_info = tk.Label(search_window, text=str(team_data), wraplength=500)
    # team_info.pack()

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

    if team['results'] > 0:
        team_info = team['response'][0]

        # Load the image from the URL
        response = requests.get(team_info['logo'])
        photo = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((50, 50)))

        # Display the image in the window
        logo = tk.Label(search_window, image=photo)
        logo.image = photo
        logo.pack()

        """Frame team"""
        frame_team = tk.Frame(search_window, bd=1, relief="solid")
        frame_team.pack(side="top", fill="x", anchor='w', padx=70, pady=20)

        title = tk.Label(frame_team, text="TEAM")
        title.grid(row=0, column=0, sticky="w")

        # Formatting the information to be displayed
        str_info = f"Name: {team_info['name']}\n" \
                   f"Nickname: {team_info['nickname']}\n" \
                   f"City: {team_info['city']}\n" \
                   f"Conference: {team_info['leagues']['standard']['conference']}\n" \
                   f"Division: {team_info['leagues']['standard']['division']}\n" \
                   f"NBA Franchise: {'Yes' if team_info['nbaFranchise'] else 'No'}\n"

        # Displaying the formatted information
        str_info_label = tk.Label(frame_team, text=str_info, justify=tk.LEFT)
        str_info_label.grid(row=1, column=0, sticky="w")

        """Frame game"""
        frame_game = tk.Frame(search_window)
        frame_game.pack()

        """Frame player"""
        frame_player = tk.Frame(search_window)
        frame_player.pack()
