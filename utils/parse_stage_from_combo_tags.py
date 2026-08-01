
def parse_stage_from_combo_tags(combo_tags):
    combo_tags = combo_tags or []
    if "Stage 1" in combo_tags or any("stage 1" in str(t).lower() for t in combo_tags):
        return "Stage 1"
    elif "Stage 2" in combo_tags or any("stage 2" in str(t).lower() for t in combo_tags):
        return "Stage 2"
    return "Basic"

