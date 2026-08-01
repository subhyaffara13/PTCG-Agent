
def test_can_serialize_dates(temp_h5_path):
    rng = [x.date() for x in bdate_range("1/1/2000", "1/30/2000")]
    frame = DataFrame(
        np.random.default_rng(2).standard_normal((len(rng), 4)), index=rng
    )

    _check_roundtrip(frame, tm.assert_frame_equal, path=temp_h5_path)

