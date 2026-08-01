
def test_ewma_halflife_without_times(halflife_with_times):
    msg = "halflife can only be a timedelta convertible argument if times is not None."
    with pytest.raises(ValueError, match=msg):
        Series(range(5)).ewm(halflife=halflife_with_times)

