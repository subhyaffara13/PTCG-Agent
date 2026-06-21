import json
import csv
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def compile_metadata(skills_dir: str = "skills"):
    s_dir = Path(skills_dir)
    raw_path = s_dir / "card_pool_raw.csv"
    score_path = s_dir / "card_scoring.json"
    out_path = s_dir / "card_metadata.json"

    metadata = {}
    
    # 1. First pass: extract stage details from raw CSV
    raw_stages = {}
    if raw_path.exists():
        try:
            with open(raw_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get("card_name", "").strip().lower()
                    raw_stages[name] = {
                        "stage_type": row.get("Stage/Type", "").strip().lower(),
                        "previous_stage": row.get("previous_stage", "").strip()
                    }
        except Exception as e:
            logger.error(f"Failed to read CSV: {e}")

    # 2. Second pass: extract lightweight data from scoring JSON
    if score_path.exists():
        try:
            data = json.loads(score_path.read_text(encoding="utf-8"))
            for c in data.get("cards", []):
                card_id_str = str(c.get("card_id", ""))
                if not card_id_str:
                    continue
                    
                name = c.get("card_name", "").strip()
                c_type_str = c.get("card_type", "Trainer")
                
                raw = raw_stages.get(name.lower(), {})
                
                metadata[card_id_str] = {
                    "card_id": card_id_str,
                    "card_name": name,
                    "card_type": c_type_str,
                    "stage_type": raw.get("stage_type", ""),
                    "previous_stage": raw.get("previous_stage", "")
                }
        except Exception as e:
            logger.error(f"Failed to read JSON: {e}")
            
    # Write metadata
    out_path.write_text(json.dumps({"cards": metadata}, indent=2), encoding="utf-8")
    logger.info(f"Successfully compiled {len(metadata)} entries into {out_path.name}")

if __name__ == "__main__":
    compile_metadata()
