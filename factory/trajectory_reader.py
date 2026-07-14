"""
factory/trajectory_reader.py

Reads compressed JSONL trajectory files written by TrajectoryLogger.
Populates the ReplayBuffer with historical experience data.
"""
import gzip
import json
import logging
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger(__name__)


class TrajectoryReader:
    def __init__(self, trajectory_dir: str = "logs/trajectories"):
        self.trajectory_dir = Path(trajectory_dir)

    def load_recent(self, max_files: int = 10) -> List[dict]:
        """Load the N most recent trajectory files, return list of match records."""
        if not self.trajectory_dir.exists():
            logger.info(f"Trajectory directory {self.trajectory_dir} does not exist.")
            return []

        # Find all trajectory files (gzipped JSONL)
        files = sorted(
            self.trajectory_dir.glob("*.jsonl.gz"),
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )
        if not files:
            # Try uncompressed
            files = sorted(
                self.trajectory_dir.glob("*.jsonl"),
                key=lambda f: f.stat().st_mtime,
                reverse=True,
            )

        files = files[:max_files]
        records = []
        for f in files:
            try:
                if f.suffix == ".gz":
                    with gzip.open(f, "rt", encoding="utf-8") as fh:
                        for line in fh:
                            line = line.strip()
                            if line:
                                records.append(json.loads(line))
                else:
                    with open(f, "r", encoding="utf-8") as fh:
                        for line in fh:
                            line = line.strip()
                            if line:
                                records.append(json.loads(line))
            except Exception as e:
                logger.warning(f"Failed to read trajectory file {f.name}: {e}")

        logger.info(f"Loaded {len(records)} trajectory records from {len(files)} files.")
        return records

    def extract_training_data(self, records: List[dict]) -> List[Tuple]:
        """Extract (state_vector, action_id, reward) tuples from trajectory records."""
        training_data = []
        for record in records:
            try:
                if "states" in record:
                    states = record["states"]
                    actions = record.get("actions", [])
                    rewards = record.get("rewards", [])
                    for i in range(min(len(states), len(actions), len(rewards))):
                        training_data.append((states[i], actions[i], rewards[i]))
                elif "state" in record:
                    training_data.append((
                        record["state"],
                        record.get("action", 0),
                        record.get("reward", 0.0),
                    ))
            except Exception as e:
                logger.debug(f"Failed to extract from record: {e}")

        logger.info(f"Extracted {len(training_data)} training samples from trajectories.")
        return training_data

    def populate_buffer(self, replay_buffer, value_network=None):
        """Read recent trajectories, optionally compute TD errors, add to replay buffer."""
        records = self.load_recent(max_files=5)
        if not records:
            return 0

        training_data = self.extract_training_data(records)
        if not training_data:
            return 0

        added = 0
        for state, action, reward in training_data:
            td_error = None
            if value_network is not None:
                try:
                    predicted_value = value_network.evaluate({"raw_state": state})
                    td_error = abs(reward - predicted_value)
                except Exception:
                    td_error = abs(reward)  # Fallback: use absolute reward as proxy

            try:
                replay_buffer.add_self_play(state, action, reward, td_error=td_error)
                added += 1
            except Exception as e:
                logger.debug(f"Failed to add to buffer: {e}")

        logger.info(f"Populated replay buffer with {added} trajectory samples.")
        return added
