
def _read_raw_stages(raw_path):
    import csv
    raw_stages = {}
    if raw_path.exists():
        try:
            with open(raw_path, "r", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    name = row.get("card_name", "").strip().lower()
                    raw_stages[name] = {"stage_type": row.get("Stage/Type", "").strip().lower(),
                                        "previous_stage": row.get("previous_stage", "").strip()}
        except Exception as e:
            logging.getLogger(__name__).error(f"Failed to read CSV: {e}")
    return raw_stages

