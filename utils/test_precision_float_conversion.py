
def test_precision_float_conversion(strrep):
    # GH 31364
    result = to_numeric(strrep)

    assert result == float(strrep)

