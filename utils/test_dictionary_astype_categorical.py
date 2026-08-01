
def test_dictionary_astype_categorical():
    # GH#56672
    arrs = [
        pa.array(np.array(["a", "x", "c", "a"])).dictionary_encode(),
        pa.array(np.array(["a", "d", "c"])).dictionary_encode(),
    ]
    ser = pd.Series(ArrowExtensionArray(pa.chunked_array(arrs)))
    result = ser.astype("category")
    categories = pd.Index(["a", "x", "c", "d"], dtype=ArrowDtype(pa.string()))
    expected = pd.Series(
        ["a", "x", "c", "a", "a", "d", "c"],
        dtype=pd.CategoricalDtype(categories=categories),
    )
    tm.assert_series_equal(result, expected)

