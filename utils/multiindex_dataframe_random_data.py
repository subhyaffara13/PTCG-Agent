
def multiindex_dataframe_random_data(
    lexsorted_two_level_string_multiindex,
) -> DataFrame:
    """DataFrame with 2 level MultiIndex with random data"""
    index = lexsorted_two_level_string_multiindex
    return DataFrame(
        np.random.default_rng(2).standard_normal((10, 3)),
        index=index,
        columns=Index(["A", "B", "C"], name="exp"),
    )

