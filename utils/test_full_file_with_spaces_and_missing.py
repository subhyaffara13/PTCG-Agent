
def test_full_file_with_spaces_and_missing():
    # File with spaces and missing values in columns.
    test = """
Account               Name    Balance     CreditLimit   AccountCreated
101                           10000.00                       1/17/1998
312     Gerard Butler         90.00       1000.00             8/6/2003
868                                                          5/25/1985
761     Jada Pinkett-Smith    49654.87    100000.00          12/5/2006
317     Bill Murray           789.65
""".strip("\r\n")
    colspecs = ((0, 7), (8, 28), (30, 38), (42, 53), (56, 70))
    expected = read_fwf(StringIO(test), colspecs=colspecs)

    result = read_fwf(StringIO(test))
    tm.assert_frame_equal(result, expected)

