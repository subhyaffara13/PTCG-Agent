def parse_stage_from_combo_tags(combo_tags):
    combo_tags = combo_tags or []
    if "Stage 1" in combo_tags or any("stage 1" in str(t).lower() for t in combo_tags):
        return "Stage 1"
    elif "Stage 2" in combo_tags or any("stage 2" in str(t).lower() for t in combo_tags):
        return "Stage 2"
    return "Basic"

def enhance_details_from_csv(details, csv_path):
    if not csv_path.exists():
        return
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
                    if prev_stage == "n/a" or not prev_stage: prev_stage = None
                    details[cid].update({"stage": stage, "previous_stage": prev_stage, "element_type": row.get("Type", "").strip()})
    except Exception as e:
        __import__('logging').getLogger(__name__).error(f"Error reading card_pool_raw.csv: {e}")
