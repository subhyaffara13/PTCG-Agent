
def save_donts(donts_file: Path, learned_donts: dict):
    try:
        donts_file.write_text(json.dumps(learned_donts, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to save learned don'ts: {e}")

