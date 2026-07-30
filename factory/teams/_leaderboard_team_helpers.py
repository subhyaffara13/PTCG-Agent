import logging
logger = logging.getLogger("LeaderboardTeam")

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

def analyze_metagame(leaderboard_entries, log_dir):
    import json
    from pathlib import Path
    meta_counts = {}
    for entry in leaderboard_entries[:20]:
        t_name = getattr(entry, 'team_name', getattr(entry, 'teamName', '')).lower()
        if "lightning" in t_name or "miraidon" in t_name: meta_counts["Lightning"] = meta_counts.get("Lightning", 0) + 1
        elif "water" in t_name or "bax" in t_name: meta_counts["Water"] = meta_counts.get("Water", 0) + 1
        elif "fire" in t_name or "zard" in t_name: meta_counts["Fire"] = meta_counts.get("Fire", 0) + 1
        else: meta_counts["Control"] = meta_counts.get("Control", 0) + 1
    dominant_meta = max(meta_counts, key=lambda k: meta_counts[k]) if meta_counts else "Lightning"
    logger.info(f"Metagame Analysis Complete. Dominant Meta: {dominant_meta} ({meta_counts.get(dominant_meta, 0)}/20 top decks)")
    meta_file = Path(log_dir) / "metagame_distribution.json"
    meta_file.write_text(json.dumps({"dominant_meta": dominant_meta, "distribution": meta_counts}, indent=2), encoding="utf-8")
    return dominant_meta
