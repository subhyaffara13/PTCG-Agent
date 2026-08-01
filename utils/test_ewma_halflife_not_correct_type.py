
def test_ewma_halflife_not_correct_type():
    msg = "halflife must be a timedelta convertible object"
    with pytest.raises(ValueError, match=msg):
        Series(range(5)).ewm(halflife=1, times=np.arange(5).astype("datetime64[ns]"))

