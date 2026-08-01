
def merge_and_save_artifacts(skills_dir, logs_dir, report_path, report_lines, deck_tips, strategy_tips, best_plays, worst_plays):
    donts_file = skills_dir / "learned_donts.json"
    existing_donts = {"deck_donts": [], "behavior_donts": []}
    if donts_file.exists():
        try:
            loaded = json.loads(donts_file.read_text(encoding="utf-8"))
            if isinstance(loaded, dict): existing_donts.update(loaded)
        except Exception: pass
    for tip in deck_tips.get("deck_donts", []):
        if not any(item.get("condition") == tip.get("condition") for item in existing_donts.get("deck_donts", [])):
            existing_donts["deck_donts"].append(tip)
    donts_file.write_text(json.dumps(existing_donts, indent=2), encoding="utf-8")
    (skills_dir / "strategy_tips.json").write_text(json.dumps(strategy_tips, indent=2), encoding="utf-8")
    pivotal = {"best_plays": best_plays[-50:], "worst_plays": worst_plays[-50:]}
    (logs_dir / "pivotal_plays.json").write_text(json.dumps(pivotal, indent=2), encoding="utf-8")
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

