
def _get_tril_sizes(row: int, col: int, offset: int) -> tuple[int, int, int]:
    if row == 0 or col == 0:
        return 0, 0, 0

    m_first_row = min(col, 1 + offset) if offset > 0 else int(row + offset > 0)
    m_last_row = max(0, min(col, row + offset))
    n_row_all = max(0, min(row, row + offset))
    n_row_trapezoid = m_last_row - m_first_row + 1

    # Number of elements in top trapezoid
    trapezoid_size = (m_first_row + m_last_row) * n_row_trapezoid // 2
    # Number of elements in bottom rectangle
    diff_row = n_row_all - n_row_trapezoid
    rectangle_size = max(0, diff_row * col)

    return trapezoid_size, rectangle_size, m_first_row

