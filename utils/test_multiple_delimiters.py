
def test_multiple_delimiters():
    test = r"""
col1~~~~~col2  col3++++++++++++++++++col4
~~22.....11.0+++foo~~~~~~~~~~Keanu Reeves
  33+++122.33\\\bar.........Gerard Butler
++44~~~~12.01   baz~~Jennifer Love Hewitt
~~55       11+++foo++++Jada Pinkett-Smith
..66++++++.03~~~bar           Bill Murray
""".strip("\r\n")
    delimiter = " +~.\\"
    colspecs = ((0, 4), (7, 13), (15, 19), (21, 41))
    expected = read_fwf(StringIO(test), colspecs=colspecs, delimiter=delimiter)

    result = read_fwf(StringIO(test), delimiter=delimiter)
    tm.assert_frame_equal(result, expected)

