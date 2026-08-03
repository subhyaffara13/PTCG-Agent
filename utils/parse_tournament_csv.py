from typing import Dict, List

def parse_tournament_csv(path: str) -> List[Dict]:
    """Parse pro match logs in CSV format."""
    samples = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                state = {"turn": int(row.get("Turn", 0))}
                action = row.get("Action", "pass")
                reward = 1.0 if row.get("Won") == "True" else 0.0
                samples.append({"state": state, "action": action, "reward": reward})
    except Exception as e:
        logger.error(f"Failed to parse CSV {path}: {e}")
    return samples

