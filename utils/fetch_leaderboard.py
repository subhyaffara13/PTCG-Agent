
def fetch_leaderboard(api, competition_id, processed_players):
    try:
        leaderboard = api.competition_leaderboard_view(competition_id)
        if not leaderboard:
            return []
        new_entries = []
        for entry in leaderboard[:50]:
            team_id = str(getattr(entry, 'team_id', getattr(entry, 'teamId', "")))
            team_name = getattr(entry, 'team_name', getattr(entry, 'teamName', ""))
            if team_id and team_id not in processed_players:
                new_entries.append((team_id, team_name))
        return new_entries
    except Exception as e:
        logger.error(f"Kaggle API or Authentication failed: {e}")
        return []

