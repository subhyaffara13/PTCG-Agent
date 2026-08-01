
def df2():
    return DataFrame(
        {
            "A": np.arange(6, dtype="int64"),
        },
        index=CategoricalIndex(
            list("aabbca"), dtype=CategoricalDtype(list("cabe")), name="B"
        ),
    )


def df2():
    return DataFrame(
        {
            "outer": [1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3],
            "inner": [1, 2, 2, 3, 3, 4, 2, 3, 1, 1, 2, 3],
            "v2": np.linspace(10, 11, 12),
        }
    )

