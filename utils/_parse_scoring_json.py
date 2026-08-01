
def _parse_scoring_json(score_path, raw_stages):
    import json, logging
    metadata = {}
    if score_path.exists():
        try:
            data = json.loads(score_path.read_text(encoding="utf-8"))
            for c in data.get("cards", []):
                card_id_str = str(c.get("card_id", ""))
                if not card_id_str: continue
                name = c.get("card_name", "").strip()
                c_type_str = c.get("card_type", "Trainer")
                raw = raw_stages.get(name.lower(), {})
                metadata[card_id_str] = {"card_id": card_id_str, "card_name": name,
                    "card_type": c_type_str, "stage_type": raw.get("stage_type", ""),
                    "previous_stage": raw.get("previous_stage", "")}
        except Exception as e:
            logging.getLogger(__name__).error(f"Failed to read JSON: {e}")
    return metadata

