
def test_resample_apply_empty_dataframe(index, freq, method):
    # GH#55572
    empty_frame_dti = DataFrame(index=index)

    rs = empty_frame_dti.resample(freq)
    result = rs.apply(getattr(rs, method))

    expected_index = _asfreq_compat(empty_frame_dti.index, freq)
    expected = DataFrame([], index=expected_index)

    tm.assert_frame_equal(result, expected)

