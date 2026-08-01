
def test_ensure_timedelta64ns_overflows():
    arr = np.arange(10).astype("m8[Y]") * 100
    msg = r"Cannot convert 300 years to timedelta64\[ns\] without overflow"
    with pytest.raises(OutOfBoundsTimedelta, match=msg):
        astype_overflowsafe(arr, dtype=np.dtype("m8[ns]"))

