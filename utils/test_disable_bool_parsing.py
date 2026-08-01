
def test_disable_bool_parsing(c_parser_only):
    # see gh-2090

    parser = c_parser_only
    data = """A,B,C
Yes,No,Yes
No,Yes,Yes
Yes,,Yes
No,No,No"""

    result = parser.read_csv(StringIO(data), dtype=object)
    assert (result.dtypes == object).all()

    result = parser.read_csv(StringIO(data), dtype=object, na_filter=False)
    assert result["B"][2] == ""

