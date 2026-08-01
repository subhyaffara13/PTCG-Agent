
def test_comment_char_in_default_value(all_parsers, request):
    # GH#34002
    if all_parsers.engine == "c":
        reason = "see gh-34002: works on the python engine but not the c engine"
        # NA value containing comment char is interpreted as comment
        request.applymarker(pytest.mark.xfail(reason=reason, raises=AssertionError))
    parser = all_parsers

    data = (
        "# this is a comment\n"
        "col1,col2,col3,col4\n"
        "1,2,3,4#inline comment\n"
        "4,5#,6,10\n"
        "7,8,#N/A,11\n"
    )
    if parser.engine == "pyarrow":
        msg = "The 'comment' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), comment="#", na_values="#N/A")
        return
    result = parser.read_csv(StringIO(data), comment="#", na_values="#N/A")
    expected = DataFrame(
        {
            "col1": [1, 4, 7],
            "col2": [2, 5, 8],
            "col3": [3.0, np.nan, np.nan],
            "col4": [4.0, np.nan, 11.0],
        }
    )
    tm.assert_frame_equal(result, expected)

