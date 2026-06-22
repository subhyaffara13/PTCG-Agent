import json
from pathlib import Path

def main():
    replay_file = Path("logs/kaggle_replays/episode-81179844-replay.json")
    data = json.loads(replay_file.read_text(encoding="utf-8"))
    
    info = data.get("info", {})
    team_names = info.get("TeamNames", ["Unknown", "Unknown"])
    agents = info.get("Agents", [])
    
    my_index = -1
    opponent_name = "Unknown"
    for idx, agent in enumerate(agents):
        name = agent.get("Name", "")
        if "Subhy" in name or "subhy" in name:
            my_index = idx
        else:
            opponent_name = name
            
    print(f"my_index: {my_index}, opponent_name: {opponent_name}")
    
    steps = data.get("steps", [])
    print(f"Num steps: {len(steps)}")
    if steps:
        last_step = steps[-1]
        rewards = [p.get("reward") for p in last_step]
        statuses = [p.get("status") for p in last_step]
        print(f"Rewards: {rewards}, Statuses: {statuses}")
        
        my_reward = rewards[my_index] if my_index != -1 else None
        print(f"my_reward: {my_reward}")

if __name__ == "__main__":
    main()
