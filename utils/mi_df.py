
def mi_df():
    return DataFrame(
        [[1, 2], [3, 4]],
        index=MultiIndex.from_product([["i0"], ["i1_a", "i1_b"]]),
        columns=MultiIndex.from_product([["c0"], ["c1_a", "c1_b"]]),
        dtype=int,
    )

