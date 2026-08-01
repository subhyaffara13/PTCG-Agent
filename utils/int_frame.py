
def int_frame() -> DataFrame:
    """
    Fixture for DataFrame of ints with index of unique strings

    Columns are ['A', 'B', 'C', 'D']
    """
    return DataFrame(
        np.ones((30, 4), dtype=np.int64),
        index=Index([f"foo_{i}" for i in range(30)]),
        columns=Index(list("ABCD")),
    )

