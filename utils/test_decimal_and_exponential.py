
def test_decimal_and_exponential(
    request, python_parser_only, numeric_decimal, thousands
):
    # GH#31920
    decimal_number_check(request, python_parser_only, numeric_decimal, thousands, None)

