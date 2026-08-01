
def test_names_and_infer_colspecs():
    # GH#45337
    data = """X   Y   Z
      959.0    345   22.2
    """
    result = read_fwf(StringIO(data), skiprows=1, usecols=[0, 2], names=["a", "b"])
    expected = DataFrame({"a": [959.0], "b": 22.2})
    tm.assert_frame_equal(result, expected)

