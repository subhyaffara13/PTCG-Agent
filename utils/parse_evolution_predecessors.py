
def parse_evolution_predecessors(csv_path):
    evolution_predecessors = {}
    if not csv_path.exists():
        return evolution_predecessors
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
    return evolution_predecessors

