
def test_bool_and_nan_to_int(all_parsers):
    # GH#42808
    parser = all_parsers
    data = """0
NaN
True
False
"""
    msg = (
        "cannot safely convert passed user dtype of int(64|32) for "
        "<class 'numpy.bool_?'> dtyped data in column 0 due to NA values"
    )
    if parser.engine == "python":
        msg = "Unable to convert column 0 to type int(64|32)"
    elif parser.engine == "pyarrow":
        msg = (
            r"int\(\) argument must be a string, a bytes-like object or a "
            "real number, not 'NoneType"
        )
    with pytest.raises(ValueError, match=msg):
        parser.read_csv(StringIO(data), dtype="int")

