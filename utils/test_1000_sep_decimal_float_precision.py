
def test_1000_sep_decimal_float_precision(
    request, c_parser_only, numeric_decimal, float_precision, thousands
):
    # test decimal and thousand sep handling in across 'float_precision'
    # parsers
    decimal_number_check(
        request, c_parser_only, numeric_decimal, thousands, float_precision
    )
    text, value = numeric_decimal
    text = " " + text + " "
    if isinstance(value, str):  # the negative cases (parse as text)
        value = " " + value + " "
    decimal_number_check(
        request, c_parser_only, (text, value), thousands, float_precision
    )

