
def _normalize_window_size(window_size: list[int] | None) -> list[int]:
    if window_size is None:
        window_size = [-1, -1]

    if len(window_size) != 2:
        raise ValueError(f"window_size must have length 2, got {len(window_size)}")
    return window_size

