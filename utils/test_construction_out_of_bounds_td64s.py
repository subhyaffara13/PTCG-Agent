
def test_construction_out_of_bounds_td64s(val, unit):
    td64 = np.timedelta64(val, unit)
    with pytest.raises(OutOfBoundsTimedelta, match=str(td64)):
        Timedelta(td64)

    # But just back in bounds and we are OK
    offset = np.timedelta64(10**9, unit)
    assert Timedelta(td64 - offset) == td64 - offset

