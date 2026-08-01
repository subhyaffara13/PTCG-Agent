
def test_ewma_times_not_datetime_type():
    msg = r"times must be datetime64 dtype."
    with pytest.raises(ValueError, match=msg):
        Series(range(5)).ewm(times=np.arange(5))

