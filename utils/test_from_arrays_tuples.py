
def test_from_arrays_tuples(idx):
    arrays = tuple(
        tuple(np.asarray(lev).take(level_codes))
        for lev, level_codes in zip(idx.levels, idx.codes, strict=True)
    )

    # tuple of tuples as input
    result = MultiIndex.from_arrays(arrays, names=idx.names)
    tm.assert_index_equal(result, idx)

