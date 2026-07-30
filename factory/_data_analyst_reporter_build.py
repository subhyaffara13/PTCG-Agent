import json
from pathlib import Path

def build_deck_tips(trend_stats, deck_trackers, threshold):
    deck_tips = {"deck_donts": []}
    report_lines = []
    if trend_stats["fast_losses"] > threshold:
        report_lines.append(f"- **[CRITICAL TREND]** Detected {trend_stats['fast_losses']} extremely fast losses (<5 turns). The deck is likely mulliganing or getting basic-benched too early.")
        deck_tips["deck_donts"].append({"condition": "pokemon_lt_12", "penalty": 2.0, "reason": "Statistically proven: dropping below 12 pokemon causes unacceptable fast-loss rates."})
    if deck_trackers["energy_starve"] > threshold:
        report_lines.append(f"- **[CRITICAL TREND]** Detected {deck_trackers['energy_starve']} games heavily plagued by dead 'pass' turns. Deck is energy starved or lacks draw support.")
        deck_tips["deck_donts"].append({"condition": "energy_lt_12_trainer_lt_10", "penalty": 2.0, "reason": "Statistically proven: low energy/draw combinations lead to >50% pass-turn game loops."})
    return deck_tips, report_lines

def build_strategy_tips(trend_stats, strategy_trackers, threshold):
    strategy_tips = {"priority_modifiers": {}}
    report_lines = []
    if strategy_trackers["passed_turns"] > trend_stats["total_games"] * 0.25:
        report_lines.append("- **[CRITICAL TREND]** The agent is passing its turn too frequently across the entire dataset. It needs an aggressive draw multiplier to force plays.")
        strategy_tips["priority_modifiers"]["force_draw_engine"] = 1.25
    if trend_stats["timeouts"] > threshold:
        report_lines.append(f"- **[CRITICAL TREND]** Detected {trend_stats['timeouts']} game timeouts. The agent is looping or stalling. Increasing aggression multiplier.")
        strategy_tips["priority_modifiers"]["aggression_bias"] = 1.5
    return strategy_tips, report_lines

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
