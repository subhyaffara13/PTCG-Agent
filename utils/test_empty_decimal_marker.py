
def test_empty_decimal_marker(all_parsers):
    data = """A|B|C
1|2,334|5
10|13|10.
"""
    # Parsers support only length-1 decimals
    msg = "Only length-1 decimal markers supported"
    parser = all_parsers

    if parser.engine == "pyarrow":
        msg = (
            "only single character unicode strings can be "
            "converted to Py_UCS4, got length 0"
        )

    with pytest.raises(ValueError, match=msg):
        parser.read_csv(StringIO(data), decimal="")

