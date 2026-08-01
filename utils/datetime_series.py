
def datetime_series() -> Series:
    """
    Fixture for Series of floats with DatetimeIndex
    """
    return Series(
        np.random.default_rng(2).standard_normal(30),
        index=date_range("2000-01-01", periods=30, freq="B"),
        name="ts",
    )

