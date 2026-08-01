
def test_factorize_dictionary_with_na():
    # GH#60567
    arr = pd.array(
        ["a1", pd.NA], dtype=ArrowDtype(pa.dictionary(pa.int32(), pa.utf8()))
    )
    indices, uniques = arr.factorize(use_na_sentinel=False)
    expected_indices = np.array([0, 1], dtype=np.intp)
    expected_uniques = pd.array(["a1", None], dtype=ArrowDtype(pa.string()))
    tm.assert_numpy_array_equal(indices, expected_indices)
    tm.assert_extension_array_equal(uniques, expected_uniques)

