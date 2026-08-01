
def best_matches(current: str, options: Collection[str], n: int) -> list[str]:
    if not current:
        return []
    # narrow down options cheaply
    options = [o for o in options if _real_quick_ratio(current, o) > 0.75]
    if len(options) >= 50:
        options = [o for o in options if abs(len(o) - len(current)) <= 1]

    ratios = {option: difflib.SequenceMatcher(a=current, b=option).ratio() for option in options}
    options = [option for option, ratio in ratios.items() if ratio > 0.75]
    return sorted(options, key=lambda v: (-ratios[v], v))[:n]

