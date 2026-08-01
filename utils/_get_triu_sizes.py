
def _get_triu_sizes(row: int, col: int, offset: int) -> tuple[int, int, int]:
    if row == 0 or col == 0:
        return 0, 0, 0

    m_first_row = max(0, col - offset) if offset > 0 else col

    # Number of elements in top rectangle
    rectangle_size = max(0, min(row, -offset) * col)

    # Number of elements in bottom trapezoid
    trapezoid_size_tril, rectangle_size_tril, _ = _get_tril_sizes(row, col, offset - 1)
    triu_size = row * col - (trapezoid_size_tril + rectangle_size_tril)
    trapezoid_size = triu_size - rectangle_size

    return trapezoid_size, rectangle_size, m_first_row

