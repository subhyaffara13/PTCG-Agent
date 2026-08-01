
def test_astype_str(using_infer_string):
    a = pd.array([0.1, 0.2, None], dtype="Float64")

    if using_infer_string:
        expected = pd.array(["0.1", "0.2", None], dtype=pd.StringDtype(na_value=np.nan))

        tm.assert_extension_array_equal(a.astype(str), expected)
        tm.assert_extension_array_equal(a.astype("str"), expected)
    else:
        expected = np.array(["0.1", "0.2", "<NA>"], dtype="U32")

        tm.assert_numpy_array_equal(a.astype(str), expected)
        tm.assert_numpy_array_equal(a.astype("str"), expected)


def test_astype_str(using_infer_string):
    a = pd.array([1, 2, None], dtype="Int64")

    if using_infer_string:
        expected = pd.array(["1", "2", None], dtype=pd.StringDtype(na_value=np.nan))

        tm.assert_extension_array_equal(a.astype(str), expected)
        tm.assert_extension_array_equal(a.astype("str"), expected)
    else:
        expected = np.array(["1", "2", "<NA>"], dtype=f"{tm.ENDIAN}U21")

        tm.assert_numpy_array_equal(a.astype(str), expected)
        tm.assert_numpy_array_equal(a.astype("str"), expected)

