
def _is_weekly(rule: str) -> bool:
    rule = rule.upper()
    return rule == "W" or rule.startswith("W-")

