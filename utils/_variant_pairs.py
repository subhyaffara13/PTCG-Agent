
def _variant_pairs(rows: list[dict], variant: str) -> dict[tuple, dict[str, float]]:
    return _pair_score_per_model([r for r in rows if r["variant"] == variant])

