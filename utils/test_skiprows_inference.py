
def test_skiprows_inference():
    # see gh-11256
    data = """
Text contained in the file header

DataCol1   DataCol2
     0.0        1.0
   101.6      956.1
""".strip()
    skiprows = 2

    expected = read_csv(StringIO(data), skiprows=skiprows, sep=r"\s+")
    result = read_fwf(StringIO(data), skiprows=skiprows)
    tm.assert_frame_equal(result, expected)

