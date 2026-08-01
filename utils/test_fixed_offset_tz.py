
def test_fixed_offset_tz(temp_hdfstore):
    rng = date_range("1/1/2000 00:00:00-07:00", "1/30/2000 00:00:00-07:00")
    frame = DataFrame(
        np.random.default_rng(2).standard_normal((len(rng), 4)), index=rng
    )

    temp_hdfstore["frame"] = frame
    recons = temp_hdfstore["frame"]
    tm.assert_index_equal(recons.index, rng)
    assert rng.tz == recons.index.tz

