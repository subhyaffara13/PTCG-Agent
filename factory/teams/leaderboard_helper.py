import json
import logging
from pathlib import Path

logger = logging.getLogger("LeaderboardHelper")

def load_processed_players(processed_file: Path) -> dict:
    if processed_file.exists():
        try:
            return json.loads(processed_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def save_processed_players(processed_file: Path, processed_players: dict):
    try:
        processed_file.write_text(json.dumps(processed_players, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to save leaderboard players: {e}")

def log_to_decisions(decisions_file: Path, team_name: str, team_id: str, wins: int, losses: int):
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"\n## Leaderboard Feedback Loop — {timestamp}\n"
        f"**Processed New Player:** {team_name} (ID: {team_id})\n"
        f"**Winning Matches Analyzed:** {wins}\n"
        f"**Losing Matches Analyzed:** {losses}\n"
        f"**Updated Skills:** Added extracted rules to `learned_dos.json` and `learned_donts.json`.\n"
        f"---\n"
    )
    try:
        with open(decisions_file, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        logger.error(f"Failed to log loop to decisions.md: {e}")

def process_team_episodes(api, team_id: str, team_name: str, scraper, do_extractor, anti_extractor) -> tuple:
    """Fetches, downloads, and analyzes wins/losses for a team."""
    subs = api.competition_team_submissions(int(team_id))
    if not subs:
        logger.warning(f"No submissions found for team {team_name} (ID: {team_id})")
        return 0, 0, None
    
    subs.sort(key=lambda s: float(getattr(s, 'public_score', getattr(s, 'publicScore', 0.0)) or 0.0), reverse=True)
    best_sub = subs[0]
    sub_id = int(getattr(best_sub, 'id', getattr(best_sub, 'submission_id', best_sub.id)))
    
    episodes = api.competition_list_episodes(sub_id)
    if not episodes:
        logger.warning(f"No episodes found for submission {sub_id}")
        return 0, 0, None
        
    wins, losses = [], []
    for ep in episodes:
        agents = getattr(ep, 'agents', [])
        ep_id = getattr(ep, 'id', None)
        if not ep_id:
            continue
        for agent in agents:
            if str(getattr(agent, 'team_id', getattr(agent, 'teamId', ''))) == team_id:
                reward = getattr(agent, 'reward', 0)
                if reward > 0:
                    wins.append(ep_id)
                elif reward < 0:
                    losses.append(ep_id)
                break
                
    downloaded_wins = [path for ep_id in wins[:5] if (path := scraper.download_episode_replay(ep_id))]
    downloaded_losses = [path for ep_id in losses[:5] if (path := scraper.download_episode_replay(ep_id))]
    
    if downloaded_wins:
        do_extractor.analyze_winning_replays(downloaded_wins, team_name)
    if downloaded_losses:
        anti_extractor.analyze_losing_replays(downloaded_losses, team_name)
        
    return len(downloaded_wins), len(downloaded_losses), sub_id
