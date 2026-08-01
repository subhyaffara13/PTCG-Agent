
def process_new_players(new_entries, api, scraper, do_extractor, anti_extractor, processed_players, processed_file, decisions_file):
    from factory.teams.leaderboard_helper import save_processed_players, log_to_decisions, process_team_episodes
    results = {"new_players_found": [], "downloaded_wins": 0, "downloaded_losses": 0}
    for team_id, team_name in new_entries:
        try:
            wins, losses, sub_id = process_team_episodes(api, team_id, team_name, scraper, do_extractor, anti_extractor)
            if sub_id is None:
                continue
            results["downloaded_wins"] += wins
            results["downloaded_losses"] += losses
            results["new_players_found"].append(team_name)
            processed_players[team_id] = {"team_name": team_name, "submission_id": sub_id, "wins_analyzed": wins, "losses_analyzed": losses}
            save_processed_players(processed_file, processed_players)
            log_to_decisions(decisions_file, team_name, team_id, wins, losses)
        except Exception as e:
            logger.error(f"Error processing team {team_name} (ID: {team_id}): {e}")
    return results

