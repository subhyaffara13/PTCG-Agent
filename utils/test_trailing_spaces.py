
def test_trailing_spaces(all_parsers, kwargs, expected_data):
    data = "A B C  \nrandom line with trailing spaces    \nskip\n1,2,3\n1,2.,4.\nrandom line with trailing tabs\t\t\t\n   \n5.1,NaN,10.0\n"  # noqa: E501
    parser = all_parsers

    if parser.engine == "pyarrow":
        with pytest.raises(ValueError, match="the 'pyarrow' engine does not support"):
            parser.read_csv(StringIO(data.replace(",", "  ")), **kwargs)
        return
    expected = DataFrame(expected_data)
    result = parser.read_csv(StringIO(data.replace(",", "  ")), **kwargs)
    tm.assert_frame_equal(result, expected)

