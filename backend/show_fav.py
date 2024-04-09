import tkinter as tk
from tkinter import ttk
import urllib.request as req
from PIL import Image, ImageTk
from tkinter import messagebox
import requests
from position import center
from api import API
from search_result import favorite_teams

def show_favorites(root):
    fav_window = tk.Toplevel(root)
    fav_window.title("Favorite Teams")
    center(fav_window)

    if not favorite_teams:
        tk.Label(fav_window, text="No favorite teams added yet.").pack()
    else:
        for team in favorite_teams:
            tk.Label(fav_window, text=team).pack()
