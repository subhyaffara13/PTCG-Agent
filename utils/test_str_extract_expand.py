
def test_str_extract_expand():
    ser = pd.Series(["a1", "b2", "c3"], dtype=ArrowDtype(pa.string()))
    result = ser.str.extract(r"[ab](?P<digit>\d)", expand=True)
    expected = pd.DataFrame(
        {
            "digit": ArrowExtensionArray(pa.array(["1", "2", None])),
        }
    )
    tm.assert_frame_equal(result, expected)

    result = ser.str.extract(r"[ab](?P<digit>\d)", expand=False)
    expected = pd.Series(ArrowExtensionArray(pa.array(["1", "2", None])), name="digit")
    tm.assert_series_equal(result, expected)

