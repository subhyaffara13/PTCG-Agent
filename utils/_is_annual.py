
def _is_annual(rule: str) -> bool:
    rule = rule.upper()
    return rule == "Y" or rule.startswith("Y-")

