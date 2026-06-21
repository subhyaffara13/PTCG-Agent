"""
factory/kaggle_scraper.py

Integrates with the official Kaggle CLI to fetch submission matches,
download replay files, and parse them for training/analytics feedback.
"""

import subprocess
import json
import logging
import csv
import io
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class KaggleScraper:
    def __init__(self, output_dir: str = "logs/kaggle_replays"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_submission_episodes(self, submission_id: int) -> List[int]:
        """
        Calls Kaggle CLI to list all episodes for a given submission ID.
        Returns a list of episode IDs.
        """
        logger.info(f"Fetching episodes for submission {submission_id} via Kaggle CLI...")
        cmd = ["kaggle", "competitions", "episodes", str(submission_id), "--csv"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = res.stdout.strip()
            if not output:
                return []
            
            # Parse CSV output
            reader = csv.DictReader(io.StringIO(output))
            episode_ids = []
            for row in reader:
                if 'id' in row:
                    try:
                        episode_ids.append(int(row['id']))
                    except ValueError:
                        pass
            logger.info(f"Found {len(episode_ids)} episodes for submission {submission_id}")
            return episode_ids
        except subprocess.CalledProcessError as e:
            logger.error(f"Kaggle CLI failed to get episodes: {e.stderr}")
            return []

    def download_episode_replay(self, episode_id: int) -> Path:
        """
        Downloads a specific episode replay JSON file.
        Returns the path to the downloaded file.
        """
        target_path = self.output_dir / f"episode-{episode_id}-replay.json"
        if target_path.exists():
            logger.info(f"Replay for episode {episode_id} already exists locally.")
            return target_path
            
        logger.info(f"Downloading replay for episode {episode_id} via Kaggle CLI...")
        cmd = ["kaggle", "competitions", "replay", str(episode_id), "-p", str(self.output_dir)]
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            # Kaggle downloads to 'episode-<episode_id>-replay.json'
            downloaded_file = self.output_dir / f"episode-{episode_id}-replay.json"
            if downloaded_file.exists():
                return downloaded_file
            logger.error(f"Replay file for episode {episode_id} was not found after download.")
            return None
        except subprocess.CalledProcessError as e:
            logger.error(f"Kaggle CLI failed to download replay: {e.stderr}")
            return None

    def parse_replay_to_history(self, replay_path: Path) -> List[Dict[str, Any]]:
        """
        Parses the downloaded Kaggle replay JSON and extracts events
        in a format compatible with the local game logs.
        """
        if not replay_path or not replay_path.exists():
            return []
            
        try:
            data = json.loads(replay_path.read_text(encoding="utf-8"))
            steps = data.get("steps", [])
            
            # Extract turn actions
            history = []
            turn_idx = 1
            for step in steps:
                # Kaggle env states are nested inside 'steps' as a list of player states
                # Player 0 and Player 1
                for idx, player_state in enumerate(step):
                    obs = player_state.get("observation", {})
                    action = player_state.get("action", [])
                    reward = player_state.get("reward", 0)
                    status = player_state.get("status", "ACTIVE")
                    
                    # Construct step trace entry
                    entry = {
                        "turn": turn_idx,
                        "player_index": idx,
                        "action_taken": action,
                        "reward": reward,
                        "status": status,
                        "my_prizes_remaining": obs.get("my_prizes", 6),
                        "opponent_prizes_remaining": obs.get("opponent_prizes", 6),
                        "my_active_hp": obs.get("my_active_hp", 100),
                        "opponent_active_hp": obs.get("opponent_active_hp", 100)
                    }
                    history.append(entry)
                turn_idx += 1
            return history
        except Exception as e:
            logger.error(f"Failed to parse replay file {replay_path}: {e}")
            return []
