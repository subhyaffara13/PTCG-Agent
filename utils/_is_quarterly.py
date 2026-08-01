
def _is_quarterly(rule: str) -> bool:
    rule = rule.upper()
    return rule == "Q" or rule.startswith(("Q-", "BQ"))

