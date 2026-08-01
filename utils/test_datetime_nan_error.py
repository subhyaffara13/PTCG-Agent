
def test_datetime_nan_error():
    msg = "bins must be of datetime64 dtype"

    with pytest.raises(ValueError, match=msg):
        cut(date_range("20130101", periods=3), bins=[0, 2, 4])

