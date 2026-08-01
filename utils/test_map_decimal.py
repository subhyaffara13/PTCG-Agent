
def test_map_decimal(string_series):
    result = string_series.map(lambda x: Decimal(str(x)))
    assert result.dtype == np.object_
    assert isinstance(result.iloc[0], Decimal)

