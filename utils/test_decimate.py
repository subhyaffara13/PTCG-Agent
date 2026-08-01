
def test_decimate():
    ones_f32 = np.ones(32, dtype=np.float32)
    assert decimate(ones_f32, 2).dtype == np.float32

    ones_i64 = np.ones(32, dtype=np.int64)
    assert decimate(ones_i64, 2).dtype == np.float64

