
def test_empty_lines(all_parsers, sep, skip_blank_lines, exp_data, request):
    parser = all_parsers
    data = """\
A,B,C
1,2.,4.


5.,NaN,10.0

-70,.4,1
"""

    if sep == r"\s+":
        data = data.replace(",", "  ")

        if parser.engine == "pyarrow":
            msg = "the 'pyarrow' engine does not support regex separators"
            with pytest.raises(ValueError, match=msg):
                parser.read_csv(
                    StringIO(data), sep=sep, skip_blank_lines=skip_blank_lines
                )
            return

    result = parser.read_csv(StringIO(data), sep=sep, skip_blank_lines=skip_blank_lines)
    expected = DataFrame(exp_data, columns=["A", "B", "C"])
    tm.assert_frame_equal(result, expected)

