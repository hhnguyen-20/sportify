# cs122-Sportify 

## Create a virtual environment
- Create a virtual environment in the root directory of the project:<br>
```terminal
python -m venv .venv
```

- Activate the virtual environment:<br>
```terminal
source .venv/bin/activate
```

## Install all libraries
- Install all libraries listed in the requirements.txt file:<br>
```terminal
pip install -r requirements.txt
```

## Run the program
- Make sure go to the app folder:<br>
```terminal
cd app
```

- Make sure API in api.py is not commented out:<br>
```python
API = "YOUR_API_KEY"
```

- Run the program:<br>
```terminal
python home.py
```

## Dependencies
- python==3.8+
- certifi==2024.2.2
- charset-normalizer==3.3.2
- idna==3.7
- pillow==10.3.0
- requests==2.31.0
- tk==0.1.0
- urllib3==2.2.1
- APIs from https://rapidapi.com/api-sports/api/api-nba
