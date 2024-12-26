from datetime import date


def format_live_game_data(live_response: dict) -> list:
    """
    Formats the live games JSON response.

    :param live_response: The JSON response for live game data
    :return: A list of formatted live matches
    """
    live_match_count = live_response.get('results', 0)
    formatted_live_matches = []

    if live_match_count == 0:
        # If no live matches
        # print("There are no live matches currently.")

        return formatted_live_matches

    for match in live_response.get('response', []):
        # Example: "LIVE - Q2-08:32"
        formatted_data = [f"LIVE - Q{match['periods']['current']}-{match['status']['clock']}",
                          str(match['teams']['visitors']['name']), match['scores']['visitors']['points'],
                          'vs.', match['scores']['home']['points'],
                          str(match['teams']['home']['name']), str(match['arena']['name']),
                          f"{str(match['arena']['city'])}, {str(match['arena']['state'])}"]
        formatted_live_matches.append(formatted_data)

    return formatted_live_matches


def format_today_game_data(today_response: dict) -> list:
    """
    Formats the JSON response for today's games.

    :param today_response: The JSON response for today's games
    :return: A list of formatted today's matches
    """
    today_match_count = today_response.get('results', 0)
    formatted_today_matches = []

    if today_match_count == 0:
        # If no matches today
        # print("There are no matches going on today")

        return formatted_today_matches

    for match in today_response.get('response', []):
        # Skip if in-play (already covered by live data)
        if match['status']['long'] == 'In Play':
            continue

        formatted_data = [str(date.today()), str(match['teams']['visitors']['name']),
                          match['scores']['visitors']['points'], 'vs.', match['scores']['home']['points'],
                          str(match['teams']['home']['name']), str(match['arena']['name']),
                          f"{str(match['arena']['city'])}, {str(match['arena']['state'])}"]
        formatted_today_matches.append(formatted_data)

    return formatted_today_matches
