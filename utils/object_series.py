
def object_series() -> Series:
    """
    Fixture for Series of dtype object with Index of unique strings
    """
    data = [f"foo_{i}" for i in range(30)]
    index = Index([f"bar_{i}" for i in range(30)])
    return Series(data, index=index, name="objects", dtype=object)

