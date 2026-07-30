from . import logger

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

