
def _is_visible(idx_row, idx_col, lengths) -> bool:
    """
    Index -> {(idx_row, idx_col): bool}).
    """
    return (idx_col, idx_row) in lengths

