
def test_skiprows_by_index_inference():
    data = """
To be skipped
Not  To  Be  Skipped
Once more to be skipped
123  34   8      123
456  78   9      456
""".strip()
    skiprows = [0, 2]

    expected = read_csv(StringIO(data), skiprows=skiprows, sep=r"\s+")
    result = read_fwf(StringIO(data), skiprows=skiprows)
    tm.assert_frame_equal(result, expected)

