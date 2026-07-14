import json
import sys
from kaggle.api.kaggle_api_extended import KaggleApi

sys.path.insert(0, "C:/Users/subhy/.gemini/antigravity/scratch/ptcg-agent")

api = KaggleApi()
api.authenticate()

sub_id = 54563959  # The complete submission from today
print(f"Fetching episodes for submission {sub_id}...")
episodes = api.competition_list_episodes(sub_id)

if not episodes:
    print("No episodes found.")
    sys.exit(0)

print(f"Found {len(episodes)} episodes.")

losses = []
errors = []
wins = 0

for ep in episodes:
    ep_id = getattr(ep, 'id', None)
    agents = getattr(ep, 'agents', [])
    for agent in agents:
        reward = getattr(agent, 'reward', 0)
        status = getattr(agent, 'status', None)
        team_id = getattr(agent, 'team_id', getattr(agent, 'teamId', ''))
        
        # We assume team_id is ours if reward is populated
        if reward > 0 and status == "DONE":
            wins += 1
        elif reward < 0:
            losses.append((ep_id, status))
        elif status in ("ERROR", "TIMEOUT", "INVALID"):
            errors.append((ep_id, status))

print(f"Summary: Wins: {wins} | Losses: {len(losses)} | Errors/Timeouts: {len(errors)}")
print("\nFirst 10 Losses:")
for ep_id, status in losses[:10]:
    print(f"  Episode {ep_id}: {status}")

print("\nFirst 10 Errors/Timeouts:")
for ep_id, status in errors[:10]:
    print(f"  Episode {ep_id}: {status}")
