
def _pad_map(map_rows, min_size=20):
    """
    Pad a small map to at least ``min_size x min_size`` by centering it in an
    ocean border, matching the upstream ``FileIO._pad_map`` behaviour.

    Args:
        map_rows: 2D list of tile code strings.
        min_size: Minimum dimension (default 20).

    Returns:
        A pandas DataFrame of the padded map.
    """
    import pandas as pd

    rows = len(map_rows)
    cols = len(map_rows[0]) if rows > 0 else 0

    if rows >= min_size and cols >= min_size:
        return pd.DataFrame(map_rows)

    new_h = max(rows, min_size)
    new_w = max(cols, min_size)

    padded = np.full((new_h, new_w), "o", dtype=object)

    offset_y = (new_h - rows) // 2
    offset_x = (new_w - cols) // 2

    for y in range(rows):
        for x in range(cols):
            padded[offset_y + y, offset_x + x] = map_rows[y][x]

    return pd.DataFrame(padded)

