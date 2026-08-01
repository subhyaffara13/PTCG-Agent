
def test_rolling_median_memory_error():
    # GH11722
    n = 20000
    Series(np.random.default_rng(2).standard_normal(n)).rolling(
        window=2, center=False
    ).median()
    Series(np.random.default_rng(2).standard_normal(n)).rolling(
        window=2, center=False
    ).median()

