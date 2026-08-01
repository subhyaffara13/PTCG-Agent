
def test_bool_and_nan_to_bool(all_parsers):
    # GH#42808
    parser = all_parsers
    data = """0
NaN
True
False
"""
    with pytest.raises(ValueError, match="NA values"):
        parser.read_csv(StringIO(data), dtype="bool")

