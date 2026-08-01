
def test_construct_from_kwargs_overflow():
    # GH#55503
    msg = "seconds=86400000000000000000, milliseconds=0, microseconds=0, nanoseconds=0"
    with pytest.raises(OutOfBoundsTimedelta, match=msg):
        Timedelta(days=10**6)
    msg = "seconds=60000000000000000000, milliseconds=0, microseconds=0, nanoseconds=0"
    with pytest.raises(OutOfBoundsTimedelta, match=msg):
        Timedelta(minutes=10**9)

