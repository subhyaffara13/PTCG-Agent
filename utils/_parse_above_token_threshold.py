
def _parse_above_token_threshold(key: str) -> float:
    threshold_str = key.split("_above_")[1].split("_tokens")[0]
    return float(threshold_str.replace("k", "")) * (1000 if "k" in threshold_str else 1)

