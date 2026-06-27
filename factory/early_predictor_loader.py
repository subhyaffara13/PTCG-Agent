import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_WEIGHTS = {
    "prize_weight": 2.0, "hand_weight": 0.5, "board_weight": 1.0,
    "energy_weight": 1.5, "active_hp_weight": 0.01,
    "evolution_combo_weight": 0.8, "trainer_utility_weight": 0.4
}

class EarlyPredictorLoader:
    def __init__(self, skills_dir: Path, weights_file: Path, feedback_file: Path):
        self.skills_dir = skills_dir
        self.weights_file = weights_file
        self.feedback_file = feedback_file

    def load_weights(self) -> dict:
        if self.weights_file.exists():
            try:
                loaded = json.loads(self.weights_file.read_text(encoding="utf-8"))
                merged = dict(DEFAULT_WEIGHTS)
                merged.update(loaded)
                return merged
            except Exception as e:
                logger.debug(f"Failed to load predictor weights (likely concurrent access): {e}")
        return dict(DEFAULT_WEIGHTS)

    def save_weights(self, weights: dict):
        try:
            self.weights_file.write_text(json.dumps(weights, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to save predictor weights: {e}")

    def load_card_pool(self) -> list:
        path = self.skills_dir / "card_scoring.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8")).get("cards", [])
            except Exception as e:
                logger.error(f"Failed to read card_scoring.json: {e}")
        return []

    def build_lookup_maps(self, card_pool: list) -> tuple[dict, dict, dict]:
        card_types = {str(c.get("card_id")): c.get("card_type", "") for c in card_pool}
        card_names = {str(c.get("card_id")): c.get("card_name", "").lower() for c in card_pool}
        evolution_predecessors = {}

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
                            evolution_predecessors[name] = prev
            except Exception as e:
                logger.error(f"Failed to parse card_pool_raw.csv: {e}")
        return card_types, card_names, evolution_predecessors

    def log_feedback(self, entry: dict):
        feedbacks = []
        if self.feedback_file.exists():
            try:
                feedbacks = json.loads(self.feedback_file.read_text(encoding="utf-8"))
                if not isinstance(feedbacks, list): feedbacks = []
            except:
                pass
        feedbacks.append(entry)
        feedbacks = feedbacks[-50:]
        try:
            self.feedback_file.write_text(json.dumps(feedbacks, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to write predictor feedback: {e}")
