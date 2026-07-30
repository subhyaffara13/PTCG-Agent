import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DeckLoader:
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir

    def load_card_pool(self) -> list:
        paths = [self.skills_dir / "card_scoring.json", Path("skills/card_scoring.json")]
        for path in paths:
            if path.exists():
                try:
                    res = json.loads(path.read_text(encoding="utf-8")).get("cards", [])
                    if res: return res
                except Exception as e:
                    logger.error(f"Failed to read {path}: {e}")
                    
        # Fallback to card_pool_raw.csv
        csv_paths = [self.skills_dir / "card_pool_raw.csv", Path("skills/card_pool_raw.csv")]
        for cp in csv_paths:
            if cp.exists():
                try:
                    import csv
                    cards = []
                    with open(cp, mode="r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        reader.fieldnames = [h.strip() for h in reader.fieldnames] if reader.fieldnames else []
                        for idx, row in enumerate(reader):
                            cid = row.get("Card ID", "").strip() or f"{idx+1}"
                            cname = row.get("Name", "").strip() or f"Card {cid}"
                            ctype = row.get("Supertype", "").strip() or "Trainer"
                            cards.append({
                                "card_id": cid,
                                "card_name": cname,
                                "card_type": ctype,
                                "archetype": "all",
                                "ev_score": 0.5
                            })
                    if cards: return cards
                except Exception as e:
                    logger.error(f"Failed to load fallback card pool from {cp}: {e}")
        return []

    def load_deck_rubric(self) -> dict:
        path = self.skills_dir / "deck_rubric.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to read deck_rubric.json: {e}")
        return {}

    def load_archetypes_data(self) -> dict:
        path = self.skills_dir / "deck_archetypes.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to read deck_archetypes.json: {e}")
        return {}

    def parse_card_details(self, card_pool: list) -> dict:
        details = {}
        for c in card_pool:
            cid = str(c.get("card_id"))
            stage = "Basic"
            combo_tags = c.get("combo_tags", [])
            if "Stage 1" in combo_tags or any("stage 1" in str(tag).lower() for tag in combo_tags):
                stage = "Stage 1"
            elif "Stage 2" in combo_tags or any("stage 2" in str(tag).lower() for tag in combo_tags):
                stage = "Stage 2"
            details[cid] = {
                "card_id": cid,
                "card_name": c.get("card_name", "Unknown"),
                "card_type": c.get("card_type", "Trainer"),
                "stage": stage,
                "previous_stage": None,
                "element_type": ""
            }

        csv_path = self.skills_dir / "card_pool_raw.csv"
        if csv_path.exists():
            try:
                import csv
                with open(csv_path, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    reader.fieldnames = [h.strip() for h in reader.fieldnames] if reader.fieldnames else []
                    stage_col = next((c for c in reader.fieldnames if "Stage" in c and "Type" in c), None)
                    for idx, row in enumerate(reader):
                        cid = row.get("Card ID", "").strip() or f"CARD-{idx}"
                        if cid in details:
                            raw_stage_type = row.get(stage_col, "").strip() if stage_col else ""
                            stage = "Stage 2" if "Stage 2" in raw_stage_type else ("Stage 1" if "Stage 1" in raw_stage_type else "Basic")
                            prev_stage = row.get("Previous stage", "").strip()
                            if prev_stage == "n/a" or not prev_stage:
                                prev_stage = None
                            details[cid].update({
                                "stage": stage,
                                "previous_stage": prev_stage,
                                "element_type": row.get("Type", "").strip()
                            })
            except Exception as e:
                logger.error(f"Error reading card_pool_raw.csv: {e}")
        return details
