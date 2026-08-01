
def test_skip_row_with_quote(all_parsers):
    # see gh-12775 and gh-10911
    parser = all_parsers
    data = """id,text,num_lines
1,"line '11' line 12",2
2,"line '21' line 22",2
3,"line '31' line 32",1"""

    exp_data = [[2, "line '21' line 22", 2], [3, "line '31' line 32", 1]]
    expected = DataFrame(exp_data, columns=["id", "text", "num_lines"])

    result = parser.read_csv(StringIO(data), skiprows=[1])
    tm.assert_frame_equal(result, expected)

