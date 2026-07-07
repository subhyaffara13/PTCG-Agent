import sys
import json
from pathlib import Path

# Add project root to sys.path
cwd = str(Path(__file__).parent.parent.resolve())
if cwd not in sys.path:
    sys.path.insert(0, cwd)

from kaggle.api.kaggle_api_extended import KaggleApi
from factory.kaggle_scraper import KaggleScraper

def main():
    if len(sys.argv) < 2:
        print("Usage: python inspect_submission_replays.py <submission_id>")
        sys.exit(1)
        
    sub_id = int(sys.argv[1])
    print(f"Retrieving episodes for submission {sub_id}...")
    
    api = KaggleApi()
    api.authenticate()
    
    try:
        episodes = api.competition_list_episodes(sub_id)
    except Exception as e:
        print(f"Failed to fetch episodes: {e}")
        sys.exit(1)
        
    if not episodes:
        print("No episodes found for this submission.")
        sys.exit(0)
        
    print(f"Found {len(episodes)} episodes.")
    
    # Let's inspect the latest 3 episodes
    scraper = KaggleScraper(output_dir="logs/kaggle_replays")
    
    for ep in list(episodes)[:3]:
        ep_id = getattr(ep, 'id', None)
        if not ep_id:
            continue
            
        print(f"\n==================================================")
        print(f"EPISODE: {ep_id}")
        print(f"==================================================")
        
        # Download replay
        p = scraper.download_episode_replay(ep_id)
        if not p or not p.exists():
            print(f"Failed to download replay for episode {ep_id}")
            continue
            
        data = json.loads(p.read_text(encoding="utf-8"))
        steps = data.get("steps", [])
        print(f"Replay steps: {len(steps)}")
        
        # Let's look for stdout/stderr logs in step 0 or 1
        # Each step is a list of player reports
        if len(steps) > 2:
            # Let's print player 0 and player 1 stderr at step 2 or 3
            for step_idx in range(min(5, len(steps))):
                step = steps[step_idx]
                print(f"\n--- STEP {step_idx} ---")
                for p_idx, player in enumerate(step):
                    action = player.get("action")
                    status = player.get("status")
                    reward = player.get("reward")
                    
                    stderr = player.get("stderr")
                    observation = player.get("observation", {}) or {}
                    logs = observation.get("logs", [])
                    
                    print(f"Player {p_idx}: status={status}, reward={reward}, action={action}")
                    if stderr:
                        print(f"Player {p_idx} Stderr:\n{stderr}")
                    if logs:
                        print(f"Player {p_idx} Observation Logs:\n{logs}")

if __name__ == "__main__":
    main()
