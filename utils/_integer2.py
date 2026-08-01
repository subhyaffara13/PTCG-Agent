
def _integer2():
    return DataFrame(
        np.random.default_rng(2).integers(1, 100, size=(101, 4)),
        columns=list("ABCD"),
        dtype="int64",
    )

