"""
factory/early_predictor.py

EarlyWinPredictor system to forecast match outcomes at turns 3-5.
Tunes itself dynamically on prediction failures.
"""

import logging
from pathlib import Path
from factory.early_predictor_loader import EarlyPredictorLoader

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
            if not isinstance(step, dict): continue
            players = step.get("players", [])
            if not players or not isinstance(players[0], dict): continue
            obs = players[0].get("observation") or {}
            curr = obs.get("current") or {}
            turn = curr.get("turn", 1)
            if turn is not None and 3 <= turn <= 5: target_step = step
            if turn is not None and turn > 5: break

        if not target_step and steps: target_step = steps[-1]
        if not target_step or not isinstance(target_step, dict): return "player_a"

        players_state = target_step.get("players", [])
        if len(players_state) < 2 or not isinstance(players_state[0], dict) or not isinstance(players_state[1], dict):
            return "player_a"

        obs = players_state[0].get("observation") or {}
        curr = obs.get("current") or {}
        players_data = curr.get("players", []) or []
        if len(players_data) < 2: return "player_a"

        scores = []
        for idx in (0, 1):
            p_data = players_data[idx]
            if not p_data or not isinstance(p_data, dict):
                scores.append(0.0)
                continue
            prizes_taken = 6 - len(p_data.get("prize", []) or [])
            hand_list = p_data.get("hand", []) or []
            active = p_data.get("active", []) or []
            bench = p_data.get("bench", []) or []
            
            energy_attached = sum(len(b.get("attached", []) or []) for b in bench if isinstance(b, dict))
            active_hp = 0
            if active and isinstance(active[0], dict):
                energy_attached += len(active[0].get("attached", []) or [])
                active_hp += active[0].get("hp", 0) or 0

            evolve_combos = trainer_utility = 0
            board_names = {self.card_names.get(str(x["id"])) for x in (active + bench) if isinstance(x, dict) and "id" in x}
            board_names.discard(None)

            for h in hand_list:
                if isinstance(h, dict) and "id" in h:
                    hid = str(h["id"])
                    if self.card_names.get(hid) in self.evolution_predecessors:
                        if self.evolution_predecessors[self.card_names[hid]] in board_names:
                            evolve_combos += 1
                    if self.card_types.get(hid) == "Trainer":
                        trainer_utility += 1

            scores.append(
                self.weights.get("prize_weight", 2.0) * prizes_taken +
                self.weights.get("hand_weight", 0.5) * len(hand_list) +
                self.weights.get("board_weight", 1.0) * (len(active) + len(bench)) +
                self.weights.get("energy_weight", 1.5) * energy_attached +
                self.weights.get("active_hp_weight", 0.01) * active_hp +
                self.weights.get("evolution_combo_weight", 0.8) * evolve_combos +
                self.weights.get("trainer_utility_weight", 0.4) * trainer_utility
            )
        return "player_a" if scores[0] >= scores[1] else "player_b"

    def upgrade(self, prediction: str, actual: str, steps: list):
        if prediction == actual or actual not in ("player_a", "player_b"): return
        direction = 1 if actual == "player_a" else -1
        feedback = {"prediction": prediction, "actual": actual, "reason": "mismatch", "weights_before": dict(self.weights)}

        lr = 0.1
        for w, scale in [("prize_weight", 0.5), ("hand_weight", 0.2), ("board_weight", 0.3), ("energy_weight", 0.4), ("evolution_combo_weight", 0.2), ("trainer_utility_weight", 0.1)]:
            self.weights[w] = max(0.1, self.weights[w] + lr * direction * scale)
        
        self.loader.save_weights(self.weights)
        feedback["weights_after"] = dict(self.weights)
        self.loader.log_feedback(feedback)
