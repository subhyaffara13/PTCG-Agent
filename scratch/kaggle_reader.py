import csv
import io
import json
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def parse_episode_csv(output: str):
    reader = csv.DictReader(io.StringIO(output))
    return [row for row in reader if row.get('id')]


def load_replay(replay_path: Path):
    try:
        return json.loads(replay_path.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning("Failed to load replay %s: %s", replay_path, e)
        return None


def download_episode_replay(episode_id: int, output_dir: Path):
    dl_cmd = ["kaggle", "competitions", "replay", str(episode_id), "-p", str(output_dir)]
    try:
        subprocess.run(dl_cmd, capture_output=True, text=True, check=True)
    except Exception as e:
        logger.warning("Failed to download episode %d: %s", episode_id, e)


def determine_result(rewards, statuses, my_index):
    my_reward = rewards[my_index] if my_index < len(rewards) else None
    my_status = statuses[my_index] if my_index < len(statuses) else None
    if my_reward is None:
        return "Unknown"
    if my_reward > 0:
        return "WIN"
    elif my_reward < 0:
        if my_status in ("ERROR", "TIMEOUT"):
            return f"LOSS ({my_status})"
        return "LOSS"
    return "DRAW"


def find_my_index(team_names, agents):
    for idx, agent in enumerate(agents):
        name = agent.get("Name", "")
        if "Subhy" in name or "subhy" in name:
            return idx
    for idx, name in enumerate(team_names):
        if "Subhy" in name or "subhy" in name:
            return idx
    return -1


def parse_episode_replay(data):
    info = data.get("info", {})
    team_names = info.get("TeamNames", ["Unknown", "Unknown"])
    agents = info.get("Agents", [])
    my_index = find_my_index(team_names, agents)
    opponent_name = team_names[1 - my_index] if my_index != -1 and len(team_names) > 1 else team_names[0] if team_names else "Unknown"
    steps = data.get("steps", [])
    num_turns = len(steps)
    win_status = "Unknown"
    if steps:
        last_step = steps[-1]
        rewards = [p.get("reward") for p in last_step]
        statuses = [p.get("status") for p in last_step]
        if my_index != -1:
            win_status = determine_result(rewards, statuses, my_index)
    return {
        "opponent": opponent_name,
        "result": win_status,
        "turns": num_turns,
        "my_index": my_index,
        "team_names": team_names,
    }
