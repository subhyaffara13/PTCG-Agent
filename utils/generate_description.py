
def generate_description(skills_dir: Path) -> str:
    desc = ["Antigravity Apex Kaggle Submission."]
    
    donts_path = skills_dir / "learned_donts.json"
    if donts_path.exists():
        try:
            donts = json.loads(donts_path.read_text(encoding="utf-8"))
            if donts.get("deck_donts"):
                desc.append("Features active Deck Architect penalties to prevent bricking patterns.")
        except:
            pass
            
    tips_path = skills_dir / "strategy_tips.json"
    if tips_path.exists():
        try:
            tips = json.loads(tips_path.read_text(encoding="utf-8"))
            if tips.get("priority_modifiers"):
                desc.append("Equipped with dynamically learned Strategy Modifiers for advanced meta play.")
        except:
            pass
            
    desc.append("Engine features MCTS Lookahead and Phase 5 Gusting/Energy-Acceleration heuristics.")
    return " ".join(desc)

