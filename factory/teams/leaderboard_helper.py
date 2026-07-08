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


def process_our_own_submissions(api, scraper, do_extractor, anti_extractor, competition_id="pokemon-tcg-ai-battle") -> tuple:
    """Fetches, downloads, and analyzes wins/losses for our own latest submissions."""
    try:
        subs = api.competition_submissions(competition_id)
        if not subs:
            return 0, 0
            
        # Sort by date (newest first)
        subs.sort(key=lambda s: getattr(s, 'date', 0), reverse=True)
        
        total_wins = 0
        total_losses = 0
        
        # Process the latest 3 submissions
        for sub in subs[:3]:
            sub_id = getattr(sub, 'ref', None)
            if not sub_id:
                for attr in ['id', 'submission_id', 'submissionId', 'key']:
                    if hasattr(sub, attr):
                        sub_id = getattr(sub, attr)
                        break
            if not sub_id:
                sub_id = vars(sub).get('ref') or vars(sub).get('id')
            if not sub_id:
                continue
                
            episodes = api.competition_list_episodes(int(sub_id))
            if not episodes:
                continue
                
            wins, losses = [], []
            for ep in episodes:
                agents = getattr(ep, 'agents', [])
                ep_id = getattr(ep, 'id', None)
                if not ep_id:
                    continue
                for agent in agents:
                    reward = getattr(agent, 'reward', 0)
                    team_id = str(getattr(agent, 'team_id', getattr(agent, 'teamId', '')))
                    if reward > 0:
                        wins.append((ep_id, team_id))
                    elif reward < 0:
                        losses.append((ep_id, team_id))
                        
            downloaded_wins = []
            for ep_id, team_id in wins[:5]:
                path = scraper.download_episode_replay(ep_id)
                if path:
                    downloaded_wins.append((path, team_id))
                    
            downloaded_losses = []
            for ep_id, team_id in losses[:5]:
                path = scraper.download_episode_replay(ep_id)
                if path:
                    downloaded_losses.append((path, team_id))
                    
            for path, team_id in downloaded_wins:
                try:
                    do_extractor.analyze_winning_replays([path], team_id)
                    total_wins += 1
                except Exception as e:
                    logger.error(f"Failed to analyze our own win replay {path}: {e}")
                    
            for path, team_id in downloaded_losses:
                try:
                    anti_extractor.analyze_losing_replays([path], team_id)
                    total_losses += 1
                except Exception as e:
                    logger.error(f"Failed to analyze our own loss replay {path}: {e}")
                    
        return total_wins, total_losses
    except Exception as e:
        logger.error(f"Failed to process our own submissions: {e}")
        return 0, 0
