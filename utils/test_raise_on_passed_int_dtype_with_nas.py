
def test_raise_on_passed_int_dtype_with_nas(all_parsers):
    # see gh-2631
    parser = all_parsers
    data = """YEAR, DOY, a
2001,106380451,10
2001,,11
2001,106380451,67"""

    if parser.engine == "c":
        msg = "Integer column has NA values"
    elif parser.engine == "pyarrow":
        msg = "The 'skipinitialspace' option is not supported with the 'pyarrow' engine"
    else:
        msg = "Unable to convert column DOY"

    with pytest.raises(ValueError, match=msg):
        parser.read_csv(StringIO(data), dtype={"DOY": np.int64}, skipinitialspace=True)

