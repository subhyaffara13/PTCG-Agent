
def _frame2():
    return DataFrame(
        np.random.default_rng(2).standard_normal((100, 4)),
        columns=list("ABCD"),
        dtype="float64",
    )

