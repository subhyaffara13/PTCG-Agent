
def test_str_split_pat_none(method):
    # GH 56271
    ser = pd.Series(["a1 cbc\nb", None], dtype=ArrowDtype(pa.string()))
    result = getattr(ser.str, method)()
    expected = pd.Series(ArrowExtensionArray(pa.array([["a1", "cbc", "b"], None])))
    tm.assert_series_equal(result, expected)

