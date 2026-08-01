
def test_arrowdtype_construct_from_string_supports_dt64tz():
    # as of GH#50689, timestamptz is supported
    dtype = ArrowDtype.construct_from_string("timestamp[s, tz=UTC][pyarrow]")
    expected = ArrowDtype(pa.timestamp("s", "UTC"))
    assert dtype == expected

