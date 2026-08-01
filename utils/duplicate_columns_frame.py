
def duplicate_columns_frame():
    """Dataframe with duplicate column names."""
    return DataFrame(
        np.random.default_rng(2).standard_normal((1500, 4)),
        columns=["a", "a", "b", "b"],
    )

