# Sportify APP

This is a simple Python application built with Tkinter that allows you to search for NBA teams and players. The
application uses the API-NBA to get the data.

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/hhnguyen-20/sportify.git
cd sportify
```

2. Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Add the [API-NBA key](https://api-sports.io) to the headers of the api_functions.py file:

`
headers = {
    'x-rapidapi-host': "v2.nba.api-sports.io",
    'x-rapidapi-key': "xxxxxxxxxxxxxxxxxxxxxx"
}
`

4. Run the app:

```bash
python home.py
```

## Create Executables

- Install PyInstaller:

```bash
pip install pyinstaller
```

- Create the executable:

```bash
pyinstaller --onefile --windowed home.py
```

- The executable will be in the `dist` folder.
