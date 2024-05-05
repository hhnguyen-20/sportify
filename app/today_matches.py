import requests
from api import API
from datetime import date


def call_game_data():
    url = "https://api-nba-v1.p.rapidapi.com/games"
    today = str(date.today())
    today_querystring = {'date': today}
    live_querystring = {'live': 'all'}
    headers = {
        "X-RapidAPI-Key": API,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    today_response = requests.get(url, headers=headers, params=today_querystring)
    live_response = requests.get(url, headers=headers, params=live_querystring)
    return today_response.json(), live_response.json()


def format_live_game_data(live_response):
    live_match_count = live_response['results']
    formatted_live_matches = []
    if live_match_count == 0:
        print("There are no live matches currently.")
    for match in live_response['response']:
        formatted_data = [f"LIVE - Q{match['periods']['current']}-{match['status']['clock']}",
                          str(match['teams']['visitors']['name']), match['scores']['visitors']['points'],
                          'vs.', match['scores']['home']['points'],
                          str(match['teams']['home']['name']), str(match['arena']['name']),
                          f"{str(match['arena']['city'])}, {str(match['arena']['state'])}"]
        formatted_live_matches.append(formatted_data)
    return formatted_live_matches


def format_today_game_data(today_response):
    today_match_count = today_response['results']
    formatted_today_matches = []
    if today_match_count == 0:
        print("There are no matches going on today")
    for match in today_response['response']:
        if match['status']['long'] == 'In Play':
            continue
        formatted_data = [str(date.today()), str(match['teams']['visitors']['name']),
                          match['scores']['visitors']['points'], 'vs.', match['scores']['home']['points'],
                          str(match['teams']['home']['name']), str(match['arena']['name']),
                          f"{str(match['arena']['city'])}, {str(match['arena']['state'])}"]
        formatted_today_matches.append(formatted_data)
    return formatted_today_matches


def main():
    today_games_json, live_games_json = call_game_data()
    live_matches = format_live_game_data(live_games_json)
    today_matches = format_today_game_data(today_games_json)


if __name__ == '__main__':
    main()
