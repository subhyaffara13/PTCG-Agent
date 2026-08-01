
def ts():
    return Series(
        np.random.default_rng(2).standard_normal(30),
        index=date_range("2000-01-01", periods=30, freq="B"),
    )


def ts():
    return Series(
        np.arange(30, dtype=np.float64),
        index=date_range("2020-01-01", periods=30, freq="B"),
        name="ts",
    )


def ts():
    return Series(
        np.arange(10, dtype=np.float64),
        index=date_range("2020-01-01", periods=10),
        name="ts",
    )

