from . import logger

def process_single_submission(sub, api, scraper, do_extractor, anti_extractor):
    sub_id = getattr(sub, 'ref', None)
    if not sub_id:
        for attr in ['id', 'submission_id', 'submissionId', 'key']:
            if hasattr(sub, attr): sub_id = getattr(sub, attr); break
    if not sub_id:
        sub_id = vars(sub).get('ref') or vars(sub).get('id')
    if not sub_id:
        return 0, 0
    episodes = api.competition_list_episodes(int(sub_id))
    if not episodes:
        return 0, 0
    wins, losses = [], []
    for ep in episodes:
        agents = getattr(ep, 'agents', [])
        ep_id = getattr(ep, 'id', None)
        if not ep_id: continue
        for agent in agents:
            reward = getattr(agent, 'reward', 0)
            team_id = str(getattr(agent, 'team_id', getattr(agent, 'teamId', '')))
            if reward > 0: wins.append((ep_id, team_id))
            elif reward < 0: losses.append((ep_id, team_id))
    total_wins = total_losses = 0
    for ep_id, team_id in wins[:5]:
        path = scraper.download_episode_replay(ep_id)
        if path:
            try: do_extractor.analyze_winning_replays([path], team_id); total_wins += 1
            except Exception as e: logger.error(f"Failed to analyze win replay {path}: {e}")
    for ep_id, team_id in losses[:5]:
        path = scraper.download_episode_replay(ep_id)
        if path:
            try: anti_extractor.analyze_losing_replays([path], team_id); total_losses += 1
            except Exception as e: logger.error(f"Failed to analyze loss replay {path}: {e}")
    return total_wins, total_losses
