
def _integer():
    return DataFrame(
        np.random.default_rng(2).integers(1, 100, size=(10001, 4)),
        columns=list("ABCD"),
        dtype="int64",
    )

