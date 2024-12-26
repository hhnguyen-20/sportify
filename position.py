def center(window):
    """
    Centers the given Tkinter window on the screen.
    :param window: The Tkinter window to be centered
    """
    window_width = 1300
    window_height = 1000
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)
    window.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
