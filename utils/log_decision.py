
def log_decision(decisions_file: Path, iteration: int, target: str, change_type: str, 
                 weak_metric: str, description: str, lines: list):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"\n## Builder Agent — Iteration {iteration} — {timestamp}\n"
        f"**Target:** {target}\n**Change type:** {change_type}\n"
        f"**Weak metric:** {weak_metric}\n**Change:** {description}\n"
        f"**Lines modified:** {lines}\n---\n"
    )
    try:
        with open(decisions_file, "a", encoding="utf-8") as f: f.write(entry)
    except Exception as e:
        logger.error(f"Failed to append builder log to decisions.md: {e}")

