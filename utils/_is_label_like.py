
def _is_label_like(val) -> bool:
    return isinstance(val, (str, tuple)) or (val is not None and is_scalar(val))

