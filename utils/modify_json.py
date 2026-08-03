import json

def modify_json(content: str, change_type: str) -> tuple[str, list[int], str]:
    data = json.loads(content)
    if change_type == "reasoning_logic" and "thresholds" in data:
        data["thresholds"]["logic_margin"] = data["thresholds"].get("logic_margin", 0.5) + 0.05
        desc = "Increased logic_margin threshold by 0.05"
    elif change_type == "priority_rules" and "attack_priority" in data:
        data["attack_priority"]["base_value"] = data["attack_priority"].get("base_value", 10) + 1
        desc = "Increased base attack_priority threshold value by 1"
    else:
        data["last_metric_tweak"] = change_type
        desc = f"Tweaked last_metric_tweak config to {change_type}"
    return json.dumps(data, indent=2), [1], desc

