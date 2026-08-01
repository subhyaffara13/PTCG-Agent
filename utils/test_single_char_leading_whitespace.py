
def test_single_char_leading_whitespace(all_parsers):
    # see gh-9710
    parser = all_parsers
    data = """\
MyColumn
a
b
a
b\n"""

    if parser.engine == "pyarrow":
        msg = "The 'skipinitialspace' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(
                StringIO(data),
                skipinitialspace=True,
            )
        return
    expected = DataFrame({"MyColumn": list("abab")})
    result = parser.read_csv(StringIO(data), skipinitialspace=True, sep=r"\s+")
    tm.assert_frame_equal(result, expected)

