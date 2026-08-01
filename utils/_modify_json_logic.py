
def _modify_json_logic(data):
    if "thresholds" in data:
        data["thresholds"]["logic_margin"] = data["thresholds"].get("logic_margin", 0.5) + 0.05
        return "Increased logic_margin threshold by 0.05"
    elif "attack_priority" in data:
        data["attack_priority"]["base_value"] = data["attack_priority"].get("base_value", 10) + 1
        return "Increased base attack_priority threshold value by 1"
    else:
        data["last_metric_tweak"] = "reasoning_logic"
        return f"Tweaked last_metric_tweak config to reasoning_logic"

