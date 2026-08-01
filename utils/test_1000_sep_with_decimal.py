
def test_1000_sep_with_decimal(
    c_parser_only, data, thousands, decimal, float_precision
):
    parser = c_parser_only
    expected = DataFrame({"A": [1, 10], "B": [2334.01, 13], "C": [5, 10.0]})

    result = parser.read_csv(
        StringIO(data),
        sep="|",
        thousands=thousands,
        decimal=decimal,
        float_precision=float_precision,
    )
    tm.assert_frame_equal(result, expected)


def test_1000_sep_with_decimal(all_parsers, data, thousands, decimal):
    parser = all_parsers
    expected = DataFrame({"A": [1, 10], "B": [2334.01, 13], "C": [5, 10.0]})

    if parser.engine == "pyarrow":
        msg = "The 'thousands' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(
                StringIO(data), sep="|", thousands=thousands, decimal=decimal
            )
        return

    result = parser.read_csv(
        StringIO(data), sep="|", thousands=thousands, decimal=decimal
    )
    tm.assert_frame_equal(result, expected)

