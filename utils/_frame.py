
def _frame():
    return DataFrame(
        np.random.default_rng(2).standard_normal((10001, 4)),
        columns=list("ABCD"),
        dtype="float64",
    )

