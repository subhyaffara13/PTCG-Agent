
def test_str_split():
    # GH 52401
    ser = pd.Series(["a1cbcb", "a2cbcb", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.split("c")
    expected = pd.Series(
        ArrowExtensionArray(pa.array([["a1", "b", "b"], ["a2", "b", "b"], None]))
    )
    tm.assert_series_equal(result, expected)

    result = ser.str.split("c", n=1)
    expected = pd.Series(
        ArrowExtensionArray(pa.array([["a1", "bcb"], ["a2", "bcb"], None]))
    )
    tm.assert_series_equal(result, expected)

    result = ser.str.split("[1-2]", regex=True)
    expected = pd.Series(
        ArrowExtensionArray(pa.array([["a", "cbcb"], ["a", "cbcb"], None]))
    )
    tm.assert_series_equal(result, expected)

    result = ser.str.split("[1-2]", regex=True, expand=True)
    expected = pd.DataFrame(
        {
            0: ArrowExtensionArray(pa.array(["a", "a", None])),
            1: ArrowExtensionArray(pa.array(["cbcb", "cbcb", None])),
        }
    )
    tm.assert_frame_equal(result, expected)

    result = ser.str.split("1", expand=True)
    expected = pd.DataFrame(
        {
            0: ArrowExtensionArray(pa.array(["a", "a2cbcb", None])),
            1: ArrowExtensionArray(pa.array(["cbcb", None, None])),
        }
    )
    tm.assert_frame_equal(result, expected)

