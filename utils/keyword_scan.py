
def keyword_scan(trigger_lower: str, profiles: dict[str, Any]) -> tuple[str | None, float]:
    best_key, best_score = None, 0.0
    for key, profile in profiles.items():
        trigger_desc = profile.get("trigger", "").lower()
        words = [w.strip("(),<>=") for w in trigger_desc.split() if len(w) > 3]
        if not words: continue
        matched = sum(1 for w in words if w in trigger_lower)
        score   = matched / len(words)
        if score > best_score:
            best_score, best_key = score, key
    return best_key, best_score


def keyword_scan(trigger_lower: str, profiles: dict[str, Any]) -> tuple[str | None, float]:
    best_key, best_score = None, 0.0
    for key, profile in profiles.items():
        trigger_desc = profile.get("trigger", "").lower()
        words = [w.strip("(),<>=") for w in trigger_desc.split() if len(w) > 3]
        if not words: continue
        matched = sum(1 for w in words if w in trigger_lower)
        score   = matched / len(words)
        if score > best_score:
            best_score, best_key = score, key
    return best_key, best_score


def keyword_scan(trigger_lower: str, profiles: dict[str, Any]) -> tuple[str | None, float]:
    best_key, best_score = None, 0.0
    for key, profile in profiles.items():
        trigger_desc = profile.get("trigger", "").lower()
        words = [w.strip("(),<>=") for w in trigger_desc.split() if len(w) > 3]
        if not words: continue
        matched = sum(1 for w in words if w in trigger_lower)
        score   = matched / len(words)
        if score > best_score:
            best_score, best_key = score, key
    return best_key, best_score

