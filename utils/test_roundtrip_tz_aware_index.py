
def test_roundtrip_tz_aware_index(temp_hdfstore, unit):
    # GH 17618
    ts = Timestamp("2000-01-01 01:00:00", tz="US/Eastern")
    dti = DatetimeIndex([ts]).as_unit(unit)
    df = DataFrame(data=[0], index=dti)

    temp_hdfstore.put("frame", df, format="fixed")
    recons = temp_hdfstore["frame"]
    tm.assert_frame_equal(recons, df)

    value = recons.index[0]._value
    denom = {"ns": 1, "us": 1000, "ms": 10**6, "s": 10**9}[unit]
    assert value == 946706400000000000 // denom

