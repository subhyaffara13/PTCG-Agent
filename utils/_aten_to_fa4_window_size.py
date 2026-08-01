
def _aten_to_fa4_window_size(val: int | None) -> int | None:
    """need to convert -1 to None for FA4"""
    return None if val == -1 else val

