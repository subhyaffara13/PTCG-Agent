
def test_maybe_infer_to_datetimelike_ser_construct():
    # see gh-19671.
    result = Series(["M1701", Timestamp("20130101")])
    assert result.dtype.kind == "O"

