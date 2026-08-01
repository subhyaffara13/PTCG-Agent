
def left_array():
    """Fixture returning boolean array with valid and missing values."""
    return pd.array([True] * 3 + [False] * 3 + [None] * 3, dtype="boolean")

