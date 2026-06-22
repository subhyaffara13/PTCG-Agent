import json
import csv
import io
import subprocess
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

def main():
    api = KaggleApi()
    api.authenticate()
    
    # Create logs/kaggle_replays and logs/kaggle_summary directories
    replays_dir = Path("logs/kaggle_replays")
    replays_dir.mkdir(parents=True, exist_ok=True)
    
    summary_dir = Path("logs/kaggle_summary")
    summary_dir.mkdir(parents=True, exist_ok=True)
    
    print("Fetching submissions...")
    subs = api.competition_submissions("pokemon-tcg-ai-battle")
    complete_subs = [s for s in subs if str(s.status) in ("SubmissionStatus.COMPLETE", "complete")]
    print(f"Found {len(complete_subs)} completed submissions.")
    
    all_results = []
    
    for s in complete_subs[:5]: # Let's process the last 5 completed submissions
        sub_id = s.ref
        sub_desc = s.description or "No description"
        print(f"\nProcessing Submission {sub_id} ({s.date})...")
        
        # Get episodes via CLI CSV output to get all fields
        cmd = ["kaggle", "competitions", "episodes", str(sub_id), "--csv"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = res.stdout.strip()
            if not output:
                print(f"No episodes found for submission {sub_id}.")
                continue
            
            reader = csv.DictReader(io.StringIO(output))
            episodes = [row for row in reader if row.get('id')]
            print(f"Found {len(episodes)} episodes.")
            
            for ep in episodes:
                ep_id = int(ep['id'])
                replay_file = replays_dir / f"episode-{ep_id}-replay.json"
                
                # Download if not exists
                if not replay_file.exists():
                    print(f"  Downloading replay for episode {ep_id}...")
                    dl_cmd = ["kaggle", "competitions", "replay", str(ep_id), "-p", str(replays_dir)]
                    subprocess.run(dl_cmd, capture_output=True, text=True, check=True)
                
                if replay_file.exists():
                    try:
                        data = json.loads(replay_file.read_text(encoding="utf-8"))
                        info = data.get("info", {})
                        team_names = info.get("TeamNames", ["Unknown", "Unknown"])
                        agents = info.get("Agents", [])
                        
                        # Find my index
                        my_index = -1
                        opponent_name = "Unknown"
                        for idx, agent in enumerate(agents):
                            name = agent.get("Name", "")
                            if "Subhy" in name or "subhy" in name:
                                my_index = idx
                            else:
                                opponent_name = name
                                
                        if my_index == -1:
                            # Fallback if name is different
                            for idx, name in enumerate(team_names):
                                if "Subhy" in name or "subhy" in name:
                                    my_index = idx
                                else:
                                    opponent_name = name
                        
                        steps = data.get("steps", [])
                        num_turns = len(steps)
                        
                        winner_index = -1
                        win_status = "Unknown"
                        
                        # Get rewards from the last step
                        if steps:
                            last_step = steps[-1]
                            rewards = [p.get("reward") for p in last_step]
                            statuses = [p.get("status") for p in last_step]
                            
                            # Reward of 1 indicates winner
                            if my_index != -1:
                                my_reward = rewards[my_index] if my_index < len(rewards) else None
                                my_status = statuses[my_index] if my_index < len(statuses) else None
                                
                                if my_reward is not None:
                                    if my_reward > 0:
                                        win_status = "WIN"
                                    elif my_reward < 0:
                                        win_status = "LOSS"
                                    else:
                                        win_status = "DRAW"
                                        
                                    if my_status == "ERROR" or my_status == "TIMEOUT":
                                        win_status = f"LOSS ({my_status})"
                            
                        all_results.append({
                            "submission_id": sub_id,
                            "submission_date": str(s.date),
                            "episode_id": ep_id,
                            "opponent": opponent_name,
                            "result": win_status,
                            "turns": num_turns,
                            "my_index": my_index,
                            "team_names": team_names
                        })
                        print(f"    Episode {ep_id}: {win_status} vs {opponent_name} ({num_turns} turns)")
                    except Exception as parse_err:
                        print(f"    Failed to parse episode {ep_id}: {parse_err}")
        except Exception as e:
            print(f"Failed to get episodes for submission {sub_id}: {e}")
            
    # Save consolidate results
    summary_file = summary_dir / "kaggle_results_summary.json"
    summary_file.write_text(json.dumps(all_results, indent=2), encoding="utf-8")
    print(f"\nSaved consolidated summary to {summary_file.resolve()}")
    
    # Print markdown table
    print("\n### SUMMARY OF KAGGLE ONLINE EPISODES")
    print("| Submission ID | Date | Episode ID | Opponent | Result | Turns |")
    print("|---|---|---|---|---|---|")
    for r in all_results[:50]: # Print top 50
        print(f"| {r['submission_id']} | {r['submission_date'][:10]} | {r['episode_id']} | {r['opponent']} | {r['result']} | {r['turns']} |")

if __name__ == "__main__":
    main()
