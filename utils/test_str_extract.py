
def test_str_extract(expand):
    ser = pd.Series(["a1", "b2", "c3"], dtype=ArrowDtype(pa.string()))
    result = ser.str.extract(r"(?P<letter>[ab])(?P<digit>\d)", expand=expand)
    expected = pd.DataFrame(
        {
            "letter": ArrowExtensionArray(pa.array(["a", "b", None])),
            "digit": ArrowExtensionArray(pa.array(["1", "2", None])),
        }
    )
    tm.assert_frame_equal(result, expected)

