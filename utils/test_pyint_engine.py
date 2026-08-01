
def test_pyint_engine(N, expected_dtype):
    # GH#18519 : when combinations of codes cannot be represented in 64
    # bits, the index underlying the MultiIndex engine works with Python
    # integers, rather than uint64.
    keys = [
        tuple(arr)
        for arr in [
            [0] * 4 * N,
            [1] * 4 * N,
            [np.nan] * N + [0] * 3 * N,
            [0] * N + [1] * 3 * N,
            [np.nan] * N + [1] * 2 * N + [0] * N,
        ]
    ]
    # Each level contains 3 elements (NaN, 0, 1), and it's represented
    # in 2 bits to store 4 possible values (0=notfound, 1=NaN, 2=0, 3=1), for
    # a total of 2*N*4 = 80 > 64 bits where N=10 and the number of levels is N*4.
    # If we were using a 64 bit engine and truncating the first levels, the
    # fourth and fifth keys would collide; if truncating the last levels, the
    # fifth and sixth; if rotating bits rather than shifting, the third and fifth.

    index = MultiIndex.from_tuples(keys)
    assert index._engine.values.dtype == expected_dtype

    for idx, key_value in enumerate(keys):
        assert index.get_loc(key_value) == idx

        expected = np.arange(idx + 1, dtype=np.intp)
        result = index.get_indexer([keys[i] for i in expected])
        tm.assert_numpy_array_equal(result, expected)

    # With missing key:
    idces = range(len(keys))
    expected = np.array([-1, *list(idces)], dtype=np.intp)
    missing = tuple([0, 1, 0, 1] * N)
    result = index.get_indexer([missing] + [keys[i] for i in idces])
    tm.assert_numpy_array_equal(result, expected)

