
def test_names_longer_than_header_but_equal_with_data_rows(all_parsers):
    # GH#38453
    parser = all_parsers
    data = """a, b
1,2,3
5,6,4
"""
    result = parser.read_csv(StringIO(data), header=0, names=["A", "B", "C"])
    expected = DataFrame({"A": [1, 5], "B": [2, 6], "C": [3, 4]})
    tm.assert_frame_equal(result, expected)

