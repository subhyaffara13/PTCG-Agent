
def _is_legacy_metric_rune(b: str, i: int) -> bool:
    return _is_legacy_labelname_rune(b, i) or b == ':'

