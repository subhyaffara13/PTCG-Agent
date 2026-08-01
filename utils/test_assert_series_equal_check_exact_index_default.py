
def test_assert_series_equal_check_exact_index_default(left_idx, right_idx):
    # GH#57067
    ser1 = Series(np.zeros(6, dtype=int), left_idx)
    ser2 = Series(np.zeros(6, dtype=int), right_idx)
    tm.assert_series_equal(ser1, ser2)
    tm.assert_frame_equal(ser1.to_frame(), ser2.to_frame())

