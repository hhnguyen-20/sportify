import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from urllib.request import urlopen
from position import center
from api_functions import call_team_data
from search_result import favorite_teams, display_data
from urllib.error import HTTPError
import PIL.Image


def show_favorites(root):
    """
    Displays the current list of favorite teams in a new window.
    """
    fav_window = tk.Toplevel(root)
    fav_window.title("Favorite Teams")
    center(fav_window)

    outer_frame = tk.Frame(fav_window)
    outer_frame.pack(expand=True, fill="both", padx=10, pady=10)

    if not favorite_teams:
        tk.Label(outer_frame, text="No favorite teams added yet.", pady=20).pack()
        return

    canvas = tk.Canvas(outer_frame)
    scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Headers
    headers = ["Roll Number", "Logo", "Team Name", "Date Added"]
    header_font = ('Arial', 14, 'bold')
    for i, header in enumerate(headers):
        label = tk.Label(scrollable_frame, text=header, font=header_font, borderwidth=2, relief="groove")
        label.grid(row=0, column=i, sticky='ew', ipadx=20, ipady=10)

    # Display the favorites data
    for index, team_item in enumerate(favorite_teams):
        roll_number, team_code, team_name, team_logo, date_added = team_item

        # Fetch and prepare the logo
        try:
            request = urlopen(team_logo)
        except HTTPError:
            image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png"
            request = urlopen(image_url)

        image = Image.open(request)
        pil_image = image.resize((50, 50), PIL.Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(pil_image)
        photo_label = tk.Label(scrollable_frame, image=photo)
        photo_label.image = photo

        # Display the data
        tk.Label(scrollable_frame, text=roll_number, font=('Arial', 12)).grid(row=index + 1, column=0, sticky='ew',
                                                                              ipadx=20, ipady=10)
        photo_label.grid(row=index + 1, column=1, sticky='ew', ipadx=20, ipady=10)
        tk.Label(scrollable_frame, text=team_name, font=('Arial', 12)).grid(row=index + 1, column=2, sticky='ew',
                                                                            ipadx=20, ipady=10)
        tk.Label(scrollable_frame, text=date_added, font=('Arial', 12)).grid(row=index + 1, column=3, sticky='ew',
                                                                             ipadx=20, ipady=10)

        # Separator after each team row
        separator = ttk.Separator(scrollable_frame, orient='horizontal')
        separator.grid(row=index + 2, column=0, columnspan=4, sticky='ew')

        # Adding a clickable event to the team name label
        team_label = tk.Label(scrollable_frame, text=team_name, font=('Arial', 12, 'underline'), fg="red",
                              cursor="hand2")
        team_label.grid(row=index + 1, column=2, sticky='ew', ipadx=20, ipady=10)
