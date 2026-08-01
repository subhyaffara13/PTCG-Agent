
def log_error_to_decisions(decisions_file: Path, reason: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n## BUILDER AGENT ERROR — {timestamp}\n**Error:** {reason}\n---\n"
    try:
        with open(decisions_file, "a", encoding="utf-8") as f: f.write(entry)
    except Exception as e:
        logger.error(f"Failed to append error to decisions.md: {e}")


def log_error_to_decisions(reason: str, decisions_file: Path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n## DECK ARCHITECT ERROR — {timestamp}\n**Error:** {reason}\n---\n"
    try:
        with open(decisions_file, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        logger.error(f"Failed to log architect error: {e}")

