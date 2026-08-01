
def analyze_metagame(leaderboard_entries, log_dir):
    import json
    from pathlib import Path
    meta_counts = {}
    for entry in leaderboard_entries[:20]:
        t_name = getattr(entry, 'team_name', getattr(entry, 'teamName', '')).lower()
        if "lightning" in t_name or "miraidon" in t_name: meta_counts["Lightning"] = meta_counts.get("Lightning", 0) + 1
        elif "water" in t_name or "bax" in t_name: meta_counts["Water"] = meta_counts.get("Water", 0) + 1
        elif "fire" in t_name or "zard" in t_name: meta_counts["Fire"] = meta_counts.get("Fire", 0) + 1
        else: meta_counts["Control"] = meta_counts.get("Control", 0) + 1
    dominant_meta = max(meta_counts, key=lambda k: meta_counts[k]) if meta_counts else "Lightning"
    logger.info(f"Metagame Analysis Complete. Dominant Meta: {dominant_meta} ({meta_counts.get(dominant_meta, 0)}/20 top decks)")
    meta_file = Path(log_dir) / "metagame_distribution.json"
    meta_file.write_text(json.dumps({"dominant_meta": dominant_meta, "distribution": meta_counts}, indent=2), encoding="utf-8")
    return dominant_meta

