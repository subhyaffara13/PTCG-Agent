"""
factory/early_predictor.py
EarlyWinPredictor system to forecast match outcomes at turns 3-5.
"""
import logging
from pathlib import Path
from factory.early_predictor_loader import EarlyPredictorLoader
from factory.early_predictor_helpers import calculate_player_score, perform_weight_upgrade

logger = logging.getLogger(__name__)

class EarlyWinPredictor:
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.loader = EarlyPredictorLoader(
            self.skills_dir,
            self.skills_dir / "predictor_weights.json",
            self.skills_dir / "predictor_feedback.json"
        )
        self.weights = self.loader.load_weights()
        self.card_pool = self.loader.load_card_pool()
        self.card_types, self.card_names, self.evolution_predecessors = self.loader.build_lookup_maps(self.card_pool)

    def _load_weights(self) -> dict:
        return self.loader.load_weights()

    def predict_winner(self, deck_a: list, deck_b: list, steps: list) -> str:
        target_step = None
        for step in steps:
            if isinstance(step, list):
                players = step
            elif isinstance(step, dict):
                players = step.get("players", [])
            else:
                continue
            if not players or not isinstance(players[0], dict): continue
            obs = players[0].get("observation") or {}
            curr = obs.get("current") or {}
            turn = curr.get("turn", 1)
            if turn is not None and 3 <= turn <= 5: target_step = step
            if turn is not None and turn > 5: break

        if not target_step and steps: target_step = steps[-1]
        if not target_step: return "player_a"

        if isinstance(target_step, list):
            players_state = target_step
        elif isinstance(target_step, dict):
            players_state = target_step.get("players", [])
        else:
            return "player_a"

        if len(players_state) < 2 or not isinstance(players_state[0], dict) or not isinstance(players_state[1], dict):
            return "player_a"

        obs = players_state[0].get("observation") or {}
        curr = obs.get("current") or {}
        players_data = curr.get("players", []) or []
        if len(players_data) < 2: return "player_a"

        scores = [
            calculate_player_score(players_data[idx], self.weights, self.card_names, self.card_types, self.evolution_predecessors)
            for idx in (0, 1)
        ]
        return "player_a" if scores[0] >= scores[1] else "player_b"

    def upgrade(self, prediction: str, actual: str, steps: list):
        if prediction == actual or actual not in ("player_a", "player_b"): return
        direction = 1 if actual == "player_a" else -1
        feedback = {"prediction": prediction, "actual": actual, "reason": "mismatch", "weights_before": dict(self.weights)}

        self.weights = perform_weight_upgrade(self.weights, direction)
        self.loader.save_weights(self.weights)
        feedback["weights_after"] = dict(self.weights)
        self.loader.log_feedback(feedback)
