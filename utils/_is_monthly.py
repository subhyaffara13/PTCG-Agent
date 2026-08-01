
def _is_monthly(rule: str) -> bool:
    rule = rule.upper()
    return rule in ("M", "BM")

