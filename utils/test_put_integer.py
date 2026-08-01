
def test_put_integer(temp_h5_path):
    # non-date, non-string index
    df = DataFrame(np.random.default_rng(2).standard_normal((50, 100)))
    _check_roundtrip(df, tm.assert_frame_equal, temp_h5_path)

