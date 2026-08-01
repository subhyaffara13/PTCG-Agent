
def test_concat_timedelta64_block():
    rng = to_timedelta(np.arange(10), unit="s")

    df = DataFrame({"time": rng})

    result = concat([df, df])
    tm.assert_frame_equal(result.iloc[:10], df, check_index_type=False)
    tm.assert_frame_equal(result.iloc[10:], df, check_index_type=False)

