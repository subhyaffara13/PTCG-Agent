
def test_construction_out_of_bounds_td64ns(val, unit):
    # TODO: parametrize over units just above/below the implementation bounds
    #  once GH#38964 is resolved

    # Timedelta.max is just under 106752 days
    td64 = np.timedelta64(val, unit)
    if is_numpy_dev or np_version_gt2_5:
        # numpy now raises instead of silently overflowing
        with pytest.raises(OverflowError, match="Overflow"):
            td64.astype("m8[ns]")
    else:
        assert td64.astype("m8[ns]").view("i8") < 0  # i.e. naive astype will be wrong

    td = Timedelta(td64)
    if unit != "M":
        # with unit="M" the conversion to "s" is poorly defined
        #  (and numpy issues DeprecationWarning)
        assert td.asm8 == td64
    assert td.asm8.dtype == "m8[s]"
    msg = r"Cannot cast 1067\d\d days .* to unit='ns' without overflow"
    with pytest.raises(OutOfBoundsTimedelta, match=msg):
        td.as_unit("ns")

    # But just back in bounds and we are OK
    one = np.timedelta64(1, unit)
    assert Timedelta(td64 - one) == td64 - one

    td64 = np.timedelta64(-val, unit)
    if is_numpy_dev or np_version_gt2_5:
        with pytest.raises(OverflowError, match="Overflow"):
            td64.astype("m8[ns]")
    else:
        assert td64.astype("m8[ns]").view("i8") > 0  # i.e. naive astype will be wrong

    td2 = Timedelta(td64)
    msg = r"Cannot cast -1067\d\d days .* to unit='ns' without overflow"
    with pytest.raises(OutOfBoundsTimedelta, match=msg):
        td2.as_unit("ns")

    # But just back in bounds and we are OK
    assert Timedelta(td64 + one) == td64 + one

