def format_data(conf_json: dict) -> dict:
    """
    Formats the JSON response of standings by extracting relevant info and
    returning a dict with the conference rank as the key.

    :param conf_json: The conference JSON response
    :return: dict with structure:
             {
                rank: [team_logo, team_nickname, wins, losses, win_percentage,
                       games_behind, home_record, away_record, last_10_record, streak]
             }
    """
    team_standing_dict = {}

    for team_info in conf_json.get('response', []):
        # Basic safety check
        if not team_info.get('team'):
            continue

        last_10_stat = f"{team_info['win']['lastTen']}-{team_info['loss']['lastTen']}"
        home_stat = f"{team_info['win']['home']}-{team_info['loss']['home']}"
        away_stat = f"{team_info['win']['away']}-{team_info['loss']['away']}"

        # Format streak (winStreak: bool, streak: number)
        if team_info.get('winStreak'):
            streak = f"W{team_info['streak']}"
        else:
            streak = f"L{team_info['streak']}"

        games_behind = team_info['gamesBehind'] if team_info['gamesBehind'] is not None else "-"

        rank = team_info['conference']['rank']
        team_standing_dict[rank] = [
            team_info['team']['logo'],
            team_info['team']['nickname'],
            team_info['conference']['win'],
            team_info['conference']['loss'],
            team_info['win']['percentage'],
            games_behind,
            home_stat,
            away_stat,
            last_10_stat,
            streak
        ]

    return team_standing_dict
