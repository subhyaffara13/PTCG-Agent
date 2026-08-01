
def string_series() -> Series:
    """
    Fixture for Series of floats with Index of unique strings
    """
    return Series(
        np.arange(30, dtype=np.float64) * 1.1,
        index=Index([f"i_{i}" for i in range(30)]),
        name="series",
    )

