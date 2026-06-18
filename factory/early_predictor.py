"""
factory/early_predictor.py

EarlyWinPredictor system to forecast match outcomes at turns 3-5.
Tunes itself dynamically on prediction failures and outputs logs for the strategy model.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

DEFAULT_WEIGHTS = {
    "prize_weight": 2.0,
    "hand_weight": 0.5,
    "board_weight": 1.0,
    "energy_weight": 1.5,
    "active_hp_weight": 0.01,
    "evolution_combo_weight": 0.8,
    "trainer_utility_weight": 0.4
}

class EarlyWinPredictor:
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.weights_file = self.skills_dir / "predictor_weights.json"
        self.feedback_file = self.skills_dir / "predictor_feedback.json"
        self.weights = self._load_weights()
        
        # Load card pool and parse lookup maps for O(1) combo evaluation
        self.card_pool = self._load_card_pool()
        self.card_types = {}
        self.card_names = {}
        self.evolution_predecessors = {}  # maps stage 1/2 card name to its previous stage name
        self._build_lookup_maps()

    def _load_card_pool(self) -> list:
        path = self.skills_dir / "card_scoring.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return data.get("cards", [])
            except Exception as e:
                logger.error(f"Failed to read card_scoring.json: {e}")
        return []

    def _build_lookup_maps(self):
        for c in self.card_pool:
            cid = str(c.get("card_id"))
            name = c.get("card_name", "").lower()
            self.card_types[cid] = c.get("card_type", "")
            self.card_names[cid] = name

        # Parse raw CSV if available to map previous stages
        csv_path = self.skills_dir / "card_pool_raw.csv"
        if csv_path.exists():
            try:
                import csv
                with open(csv_path, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        name = row.get("card_name", "").strip().lower()
                        prev = row.get("previous_stage", "").strip().lower()
                        if name and prev and prev != "none":
                            self.evolution_predecessors[name] = prev
            except Exception as e:
                logger.error(f"Failed to parse card_pool_raw.csv: {e}")

    def _load_weights(self) -> dict:
        if self.weights_file.exists():
            try:
                # Merge loaded weights with DEFAULT_WEIGHTS to ensure compatibility with new combo weights
                loaded = json.loads(self.weights_file.read_text(encoding="utf-8"))
                merged = dict(DEFAULT_WEIGHTS)
                merged.update(loaded)
                return merged
            except Exception as e:
                logger.error(f"Failed to load predictor weights: {e}")
        return dict(DEFAULT_WEIGHTS)

    def _save_weights(self):
        try:
            self.weights_file.write_text(json.dumps(self.weights, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to save predictor weights: {e}")

    def predict_winner(self, deck_a: list, deck_b: list, steps: list) -> str:
        """
        Analyzes the game steps up to turn 5 and predicts the winner.
        """
        target_step = None
        for step in steps:
            if not isinstance(step, dict):
                continue
            players = step.get("players", [])
            if not players:
                continue
            
            p0 = players[0]
            if not isinstance(p0, dict):
                continue
                
            obs = p0.get("observation", {})
            if not obs:
                continue
                
            current = obs.get("current", {})
            if not current:
                continue
                
            turn = current.get("turn", 1)
            if turn is not None and 3 <= turn <= 5:
                target_step = step
            if turn is not None and turn > 5:
                break

        if not target_step and steps:
            target_step = steps[-1]

        if not target_step or not isinstance(target_step, dict):
            return "player_a"

        players_state = target_step.get("players", [])
        if len(players_state) < 2:
            return "player_a"

        p0_state = players_state[0]
        p1_state = players_state[1]
        if not isinstance(p0_state, dict) or not isinstance(p1_state, dict):
            return "player_a"

        p0_obs = p0_state.get("observation", {}) or {}
        current_p0 = p0_obs.get("current", {}) or {}
        players_data = current_p0.get("players", []) or []
        if len(players_data) < 2:
            return "player_a"

        scores = []
        for idx in (0, 1):
            p_data = players_data[idx]
            if not p_data or not isinstance(p_data, dict):
                scores.append(0.0)
                continue
                
            prize_list = p_data.get("prize", []) or []
            prizes_taken = 6 - len(prize_list)
            
            hand_list = p_data.get("hand", []) or []
            hand_size = len(hand_list)
            
            active = p_data.get("active", []) or []
            bench = p_data.get("bench", []) or []
            board_size = len(active) + len(bench)
            
            energy_attached = 0
            active_hp = 0
            if active and isinstance(active[0], dict):
                energy_attached += len(active[0].get("attached", []) or [])
                active_hp += active[0].get("hp", 0) or 0
                
            for b in bench:
                if isinstance(b, dict):
                    energy_attached += len(b.get("attached", []) or [])

            # Compute evolution combos and trainer utility using O(1) sets
            evolve_combos = 0
            trainer_utility = 0
            
            board_names = set()
            for act in active:
                if isinstance(act, dict) and "id" in act:
                    name = self.card_names.get(str(act["id"]))
                    if name:
                        board_names.add(name)
            for bnc in bench:
                if isinstance(bnc, dict) and "id" in bnc:
                    name = self.card_names.get(str(bnc["id"]))
                    if name:
                        board_names.add(name)

            for h in hand_list:
                if isinstance(h, dict) and "id" in h:
                    hid = str(h["id"])
                    hname = self.card_names.get(hid)
                    htype = self.card_types.get(hid)
                    
                    if hname in self.evolution_predecessors:
                        pred_name = self.evolution_predecessors[hname]
                        if pred_name in board_names:
                            evolve_combos += 1
                    
                    if htype == "Trainer":
                        trainer_utility += 1

            score = (
                self.weights.get("prize_weight", 2.0) * prizes_taken +
                self.weights.get("hand_weight", 0.5) * hand_size +
                self.weights.get("board_weight", 1.0) * board_size +
                self.weights.get("energy_weight", 1.5) * energy_attached +
                self.weights.get("active_hp_weight", 0.01) * active_hp +
                self.weights.get("evolution_combo_weight", 0.8) * evolve_combos +
                self.weights.get("trainer_utility_weight", 0.4) * trainer_utility
            )
            scores.append(score)

        return "player_a" if scores[0] >= scores[1] else "player_b"

    def upgrade(self, prediction: str, actual: str, steps: list):
        """
        Dynamically adjusts weights if the prediction was wrong.
        """
        if prediction == actual or actual not in ("player_a", "player_b"):
            return

        direction = 1 if actual == "player_a" else -1
        
        feedback = {
            "prediction": prediction,
            "actual": actual,
            "reason": "mismatch",
            "weights_before": dict(self.weights)
        }

        lr = 0.1
        self.weights["prize_weight"] = max(0.1, self.weights["prize_weight"] + lr * direction * 0.5)
        self.weights["hand_weight"] = max(0.1, self.weights["hand_weight"] + lr * direction * 0.2)
        self.weights["board_weight"] = max(0.1, self.weights["board_weight"] + lr * direction * 0.3)
        self.weights["energy_weight"] = max(0.1, self.weights["energy_weight"] + lr * direction * 0.4)
        self.weights["evolution_combo_weight"] = max(0.1, self.weights["evolution_combo_weight"] + lr * direction * 0.2)
        self.weights["trainer_utility_weight"] = max(0.1, self.weights["trainer_utility_weight"] + lr * direction * 0.1)
        
        self._save_weights()

        feedback["weights_after"] = dict(self.weights)
        self._log_feedback(feedback)

    def _log_feedback(self, entry: dict):
        feedbacks = []
        if self.feedback_file.exists():
            try:
                feedbacks = json.loads(self.feedback_file.read_text(encoding="utf-8"))
                if not isinstance(feedbacks, list):
                    feedbacks = []
            except:
                pass
        
        feedbacks.append(entry)
        feedbacks = feedbacks[-50:]
        try:
            self.feedback_file.write_text(json.dumps(feedbacks, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to write predictor feedback: {e}")
