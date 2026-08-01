
def test_quantile_temporal(pa_type):
    # GH52678
    data = [1, 2, 3]
    ser = pd.Series(data, dtype=ArrowDtype(pa_type))
    result = ser.quantile(0.1)
    expected = ser[0]
    assert result == expected

