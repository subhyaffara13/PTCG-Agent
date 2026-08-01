
def test_tseries_select_index_column(temp_hdfstore):
    # GH7777
    # selecting a UTC datetimeindex column did
    # not preserve UTC tzinfo set before storing

    # check that no tz still works
    rng = date_range("1/1/2000", "1/30/2000")
    frame = DataFrame(
        np.random.default_rng(2).standard_normal((len(rng), 4)), index=rng
    )

    temp_hdfstore.append("frame", frame)
    result = temp_hdfstore.select_column("frame", "index")
    assert rng.tz == DatetimeIndex(result.values).tz

    # check utc
    rng = date_range("1/1/2000", "1/30/2000", tz="UTC")
    frame = DataFrame(
        np.random.default_rng(2).standard_normal((len(rng), 4)), index=rng
    )

    temp_hdfstore.remove("frame")
    temp_hdfstore.append("frame", frame)
    result = temp_hdfstore.select_column("frame", "index")
    assert rng.tz == result.dt.tz

    # double check non-utc
    rng = date_range("1/1/2000", "1/30/2000", tz="US/Eastern")
    frame = DataFrame(
        np.random.default_rng(2).standard_normal((len(rng), 4)), index=rng
    )

    temp_hdfstore.remove("frame")
    temp_hdfstore.append("frame", frame)
    result = temp_hdfstore.select_column("frame", "index")
    assert rng.tz == result.dt.tz

