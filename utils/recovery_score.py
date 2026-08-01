
def recovery_score(ct: dict) -> float:
    try:
        rs = min(1.0, ct.get("sup", 0) / 15.0)
        return min(1.0, rs + 0.1) if ct.get("rec", 0) >= 2 else (max(0.0, rs - 0.1) if ct.get("rec", 0) == 0 else rs)
    except Exception:
        return 0.0

