import json
import pathlib
import sys
import os
import time

# Add project root to sys.path
sys.path.insert(0, "C:/Users/subhy/.gemini/antigravity/scratch/ptcg-agent")

from kaggle.api.kaggle_api_extended import KaggleApi
from factory.anti_pattern_extractor import AntiPatternExtractor
from factory.kaggle_scraper import KaggleScraper

def main():
    print("[Audit] Initializing Kaggle API...")
    try:
        api = KaggleApi()
        api.authenticate()
    except Exception as e:
        print(f"[Audit] Kaggle authentication failed: {e}")
        return
        
    print("[Audit] Fetching our submissions for pokemon-tcg-ai-battle...")
    try:
        subs = api.competition_submissions("pokemon-tcg-ai-battle")
    except Exception as e:
        print(f"[Audit] Failed to fetch submissions: {e}")
        return
        
    if not subs:
        print("[Audit] No submissions found.")
        return
        
    # Sort submissions by date (newest first)
    subs.sort(key=lambda s: s.date, reverse=True)
    latest_sub = subs[0]
    print("[Audit] Inspecting latest submission attributes:")
    for attr in dir(latest_sub):
        if not attr.startswith('_'):
            try:
                print(f"  {attr}: {getattr(latest_sub, attr)}")
            except Exception:
                pass
    sub_id = getattr(latest_sub, 'ref', None)
    if not sub_id:
        for attr in ['id', 'submission_id', 'submissionId', 'key']:
            if hasattr(latest_sub, attr):
                sub_id = getattr(latest_sub, attr)
                break
    sub_id = 54563959
    print(f"[Audit] Selected sub_id: {sub_id}")
    
    print(f"[Audit] Fetching episodes for submission {sub_id}...")
    try:
        episodes = api.competition_list_episodes(sub_id)
    except Exception as e:
        print(f"[Audit] Failed to fetch episodes: {e}")
        return
        
    if not episodes:
        print("[Audit] No episodes found for the latest submission.")
        return
        
    print(f"[Audit] Found {len(episodes)} episodes. Searching for losses...")
    
    # We want to identify the team ID and find the episodes where reward was negative (loss)
    # To find our team name/id, we check the agents list
    our_team_id = None
    losses = []
    
    for ep in episodes:
        agents = getattr(ep, 'agents', [])
        ep_id = getattr(ep, 'id', None)
        if not ep_id:
            continue
            
        # Check rewards
        for agent in agents:
            reward = getattr(agent, 'reward', 0)
            team_id = str(getattr(agent, 'team_id', getattr(agent, 'teamId', '')))
            
            # Since this is our submission, we find our team_id by matching reward signs or agent index
            # Let's check if reward is -1 (loss)
            if reward < 0:
                losses.append((ep_id, team_id))
                our_team_id = team_id
                
    if not losses:
        print("[Audit] No losses found in the latest episodes! Excellent job! (Or all games are wins/draws).")
        return
        
    print(f"[Audit] Found {len(losses)} losses. We will analyze the latest 3 losses.")
    scraper = KaggleScraper(output_dir="logs/kaggle_replays")
    extractor = AntiPatternExtractor(logs_dir="logs", skills_dir="skills")
    
    analyzed_count = 0
    for ep_id, team_id in losses[:3]:
        print(f"\n--- Analyzing Loss Replay (Episode {ep_id}) ---")
        path = scraper.download_episode_replay(ep_id)
        if path and path.exists():
            try:
                # Run the anti-pattern extraction
                extractor.analyze_losing_replays([path], team_id)
                
                # Load replay to print high-level info
                with open(path, "r", encoding="utf-8") as f:
                    replay = json.load(f)
                steps = replay.get("steps", [])
                print(f"  Replay parsed successfully: {len(steps)} steps.")
                
                # Check player index
                info = replay.get("info", {})
                team_names = info.get("TeamNames", ["", ""])
                player_idx = -1
                for idx, name in enumerate(team_names):
                    # Check if team matches
                    if str(team_id) in name or any(part in name.lower() for part in ["subhy", "antigravity", "apex"]):
                        player_idx = idx
                        break
                if player_idx == -1:
                    # Fallback check
                    for idx, p_state in enumerate(steps[1] if len(steps) > 1 else []):
                        obs_dict = p_state.get("observation") or {}
                        current = obs_dict.get("current") or {}
                        players = current.get("players", [])
                        if idx < len(players) and str(players[idx].get("teamId")) == str(team_id):
                            player_idx = idx
                            break
                            
                if player_idx != -1:
                    opp_idx = 1 - player_idx
                    opp_name = team_names[opp_idx] if opp_idx < len(team_names) else "Opponent"
                    print(f"  We were Player {player_idx}. Opponent: {opp_name}")
                    
                    # Print why we lost (e.g. prizes remaining, timeouts, etc.)
                    final_step = steps[-1]
                    if len(final_step) > player_idx:
                        our_reward = final_step[player_idx].get("reward", 0)
                        opp_reward = final_step[opp_idx].get("reward", 0)
                        obs = final_step[player_idx].get("observation", {}) or {}
                        current = obs.get("current") or {}
                        players = current.get("players", [])
                        if len(players) > player_idx:
                            our_prizes = len(players[player_idx].get("prize", []))
                            opp_prizes = len(players[opp_idx].get("prize", []))
                            print(f"  Prizes remaining - Us: {our_prizes}, Opponent: {opp_prizes}")
                            
                        # Look at the status
                        status = final_step[player_idx].get("status")
                        print(f"  Our final status: {status}")
                analyzed_count += 1
            except Exception as e:
                print(f"  Error during replay analysis: {e}")
        else:
            print(f"  Failed to download replay for episode {ep_id}")
            
    print(f"\n[Audit] Finished auditing {analyzed_count} losses.")
    
    # Audit evolved learned_donts
    donts_path = pathlib.Path("skills/learned_donts.json")
    if donts_path.exists():
        with open(donts_path, "r", encoding="utf-8") as f:
            donts = json.load(f)
        print("\n--- Current Learned Don'ts ---")
        print(json.dumps(donts, indent=2))
    else:
        print("[Audit] learned_donts.json does not exist.")

if __name__ == "__main__":
    main()
