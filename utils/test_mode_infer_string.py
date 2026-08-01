
def test_mode_infer_string():
    # GH#56183
    pytest.importorskip("pyarrow")
    ser = Series(["a", "b"], dtype=object)
    with pd.option_context("future.infer_string", True):
        result = ser.mode()
    expected = Series(["a", "b"], dtype=object)
    tm.assert_series_equal(result, expected)

