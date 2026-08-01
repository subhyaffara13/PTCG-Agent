
def test_invalid_quantile_value():
    data = np.arange(5)
    s = Series(data)

    msg = "Interpolation 'invalid' is not supported"
    with pytest.raises(ValueError, match=msg):
        s.rolling(len(data), min_periods=1).quantile(0.5, interpolation="invalid")

