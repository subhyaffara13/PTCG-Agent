
def test_numpy_ufuncs_out(index):
    result = index == index

    out = np.empty(index.shape, dtype=bool)
    np.equal(index, index, out=out)
    tm.assert_numpy_array_equal(out, result)

    if not index._is_multi:
        # same thing on the ExtensionArray
        out = np.empty(index.shape, dtype=bool)
        np.equal(index.array, index.array, out=out)
        tm.assert_numpy_array_equal(out, result)

