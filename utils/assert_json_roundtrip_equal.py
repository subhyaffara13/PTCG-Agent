
def assert_json_roundtrip_equal(result, expected, orient):
    if orient in ("records", "values"):
        expected = expected.reset_index(drop=True)
    if orient == "values":
        expected.columns = range(len(expected.columns))
    tm.assert_frame_equal(result, expected)

