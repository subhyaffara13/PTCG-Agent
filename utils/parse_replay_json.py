
def parse_replay_json(path: str) -> List[Dict]:
    """Parse game replay JSON."""
    samples = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for step in data.get("steps", []):
                state = step.get("state", {})
                action = step.get("action", "pass")
                reward = step.get("reward", 0.0)
                samples.append({"state": state, "action": action, "reward": reward})
    except Exception as e:
        logger.error(f"Failed to parse JSON {path}: {e}")
    return samples

