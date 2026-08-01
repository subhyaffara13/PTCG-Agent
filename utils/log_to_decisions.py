
def log_to_decisions(decisions_file: Path, team_name: str, team_id: str, wins: int, losses: int):
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"\n## Leaderboard Feedback Loop — {timestamp}\n"
        f"**Processed New Player:** {team_name} (ID: {team_id})\n"
        f"**Winning Matches Analyzed:** {wins}\n"
        f"**Losing Matches Analyzed:** {losses}\n"
        f"**Updated Skills:** Added extracted rules to `learned_dos.json` and `learned_donts.json`.\n"
        f"---\n"
    )
    try:
        with open(decisions_file, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        logger.error(f"Failed to log loop to decisions.md: {e}")

