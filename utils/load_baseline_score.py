
def load_baseline_score(history_file: Path) -> float:
    if history_file.exists():
        try:
            history = json.loads(history_file.read_text(encoding="utf-8").strip())
            if history:
                scores = [item.get("version_score", 0.0) for item in history if item.get("promoted") is True]
                if scores: return max(scores)
        except Exception as e:
            logger.error(f"Failed to load baseline score: {e}")
    return 0.0

