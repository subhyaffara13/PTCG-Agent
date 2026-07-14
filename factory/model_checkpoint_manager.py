"""
factory/model_checkpoint_manager.py

Manages neural network snapshots for league training.
Saves periodic checkpoints, tracks their Elo, and provides random opponent loading.
"""
import json
import shutil
import logging
import random
import time
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class ModelCheckpointManager:
    def __init__(self, checkpoint_dir: str = "models/league", max_checkpoints: int = 20):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.max_checkpoints = max_checkpoints
        self.registry_path = self.checkpoint_dir / "checkpoint_registry.json"
        self.registry = self._load_registry()
        self.K = 32  # Standard Elo K-factor

    def _load_registry(self) -> list:
        if self.registry_path.exists():
            try:
                data = json.loads(self.registry_path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    return data
            except Exception as e:
                logger.warning(f"Failed to load checkpoint registry: {e}")
        return []

    def _save_registry(self):
        try:
            self.registry_path.write_text(
                json.dumps(self.registry, indent=2), encoding="utf-8"
            )
        except Exception as e:
            logger.error(f"Failed to save checkpoint registry: {e}")

    def save_checkpoint(self, model_path: str, iteration: int) -> Optional[str]:
        """Copy current model to models/league/checkpoint_iter_{N}.pt.
        Register with starting Elo 1200. Prune if over limit."""
        src = Path(model_path)
        if not src.exists():
            logger.warning(f"Model file {model_path} does not exist. Cannot checkpoint.")
            return None

        checkpoint_name = f"checkpoint_iter_{iteration:04d}.pt"
        dest = self.checkpoint_dir / checkpoint_name

        # Don't re-checkpoint the same iteration
        if any(c["iteration"] == iteration for c in self.registry):
            logger.debug(f"Checkpoint for iteration {iteration} already exists. Skipping.")
            return str(dest)

        try:
            shutil.copy2(str(src), str(dest))
            entry = {
                "id": checkpoint_name,
                "path": str(dest),
                "iteration": iteration,
                "elo": 1200.0,
                "timestamp": time.time(),
                "games_played": 0,
            }
            self.registry.append(entry)
            self._save_registry()
            logger.info(f"Saved checkpoint: {checkpoint_name} (Elo: 1200)")

            # Prune if over limit
            self.prune()
            return str(dest)
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
            return None

    def load_random_opponent(self) -> Optional[Tuple]:
        """Load a random past checkpoint, weighted toward similar Elo.
        Returns (model_path, checkpoint_info) or None."""
        if not self.registry:
            return None

        # Weight selection toward middle Elo (more useful training signal)
        weights = []
        avg_elo = sum(c["elo"] for c in self.registry) / len(self.registry)
        for c in self.registry:
            # Gaussian-like weighting around average Elo
            diff = abs(c["elo"] - avg_elo)
            weight = max(0.1, 1.0 - diff / 400.0)
            weights.append(weight)

        total = sum(weights)
        weights = [w / total for w in weights]

        chosen = random.choices(self.registry, weights=weights, k=1)[0]
        checkpoint_path = Path(chosen["path"])
        if not checkpoint_path.exists():
            logger.warning(f"Checkpoint file missing: {chosen['path']}")
            return None

        return (str(checkpoint_path), chosen)

    def update_checkpoint_elo(self, checkpoint_id: str, opponent_elo: float, result: float):
        """Update Elo after a match. result: 1.0=checkpoint wins, 0.0=opponent wins, 0.5=draw."""
        cp = next((c for c in self.registry if c["id"] == checkpoint_id), None)
        if cp is None:
            return

        ea = 1.0 / (1.0 + 10 ** ((opponent_elo - cp["elo"]) / 400.0))

        cp["elo"] += self.K * (result - ea)
        cp["games_played"] = cp.get("games_played", 0) + 1

        self._save_registry()

    def get_registry(self) -> list:
        """Return all checkpoints sorted by Elo descending."""
        return sorted(self.registry, key=lambda c: c["elo"], reverse=True)

    def prune(self):
        """Remove lowest-Elo checkpoints beyond max. Never delete the highest-Elo one."""
        if len(self.registry) <= self.max_checkpoints:
            return

        sorted_reg = sorted(self.registry, key=lambda c: c["elo"])
        to_remove = sorted_reg[: len(sorted_reg) - self.max_checkpoints]

        # Never remove the best
        best_id = sorted_reg[-1]["id"]
        to_remove = [c for c in to_remove if c["id"] != best_id]

        for c in to_remove:
            try:
                Path(c["path"]).unlink(missing_ok=True)
                self.registry.remove(c)
                logger.info(f"Pruned checkpoint {c['id']} (Elo: {c['elo']:.0f})")
            except Exception as e:
                logger.warning(f"Failed to prune {c['id']}: {e}")

        self._save_registry()
