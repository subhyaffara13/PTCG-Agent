
def _models_in(rows: list[dict]) -> list[str]:
    seen = set()
    for r in rows:
        seen.add(r["model_p0"])
        seen.add(r["model_p1"])
    return sorted(seen)

