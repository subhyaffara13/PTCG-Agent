"""
factory/kaggle_scraper.py

Integrates with the official Kaggle CLI to fetch submission matches,
download replay files, and parse them for training/analytics feedback. Kept under 100 lines.
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
        """Calls Kaggle CLI to list all episodes for a given submission ID."""
        logger.info(f"Fetching episodes for submission {submission_id} via Kaggle CLI...")
        cmd = ["kaggle", "competitions", "episodes", str(submission_id), "--csv"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = res.stdout.strip()
            if not output:
                return []
            reader = csv.DictReader(io.StringIO(output))
            return [int(row['id']) for row in reader if 'id' in row and row['id'].isdigit()]
        except Exception as e:
            logger.error(f"Kaggle CLI failed to get episodes: {e}")
            return []

    def download_episode_replay(self, episode_id: int) -> Path | None:
        """Downloads a specific episode replay JSON file."""
        target_path = self.output_dir / f"episode-{episode_id}-replay.json"
        if target_path.exists():
            logger.info(f"Replay for episode {episode_id} already exists locally.")
            return target_path
            
        logger.info(f"Downloading replay for episode {episode_id} via Kaggle CLI...")
        cmd = ["kaggle", "competitions", "replay", str(episode_id), "-p", str(self.output_dir)]
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            downloaded_file = self.output_dir / f"episode-{episode_id}-replay.json"
            return downloaded_file if downloaded_file.exists() else None
        except Exception as e:
            logger.error(f"Kaggle CLI failed to download replay: {e}")
            return None

    def parse_replay_to_history(self, replay_path: Path) -> List[Dict[str, Any]]:
        """Parses the downloaded Kaggle replay JSON and extracts events."""
        if not replay_path or not replay_path.exists():
            return []
            
        try:
            data = json.loads(replay_path.read_text(encoding="utf-8"))
            steps = data.get("steps", [])
            history = []
            for turn_idx, step in enumerate(steps, start=1):
                for idx, player_state in enumerate(step):
                    obs = player_state.get("observation", {}) or {}
                    history.append({
                        "turn": turn_idx,
                        "player_index": idx,
                        "action_taken": player_state.get("action", []),
                        "reward": player_state.get("reward", 0),
                        "status": player_state.get("status", "ACTIVE"),
                        "my_prizes_remaining": obs.get("my_prizes", 6),
                        "opponent_prizes_remaining": obs.get("opponent_prizes", 6),
                        "my_active_hp": obs.get("my_active_hp", 100),
                        "opponent_active_hp": obs.get("opponent_active_hp", 100)
                    })
            return history
        except Exception as e:
            logger.error(f"Failed to parse replay file {replay_path}: {e}")
            return []
