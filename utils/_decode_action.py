
def _decode_action(action: int, num_rows: int, num_cols: int) -> tuple[str, int, int]:
    max_h = (num_rows + 1) * num_cols
    if action < max_h:
        return "h", action // num_cols, action % num_cols
    action -= max_h
    return "v", action // (num_cols + 1), action % (num_cols + 1)

