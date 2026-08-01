
def test_memoverlap_accumulate(ftype):
    # Reproduces bug https://github.com/numpy/numpy/issues/15597
    arr = np.array([0.61, 0.60, 0.77, 0.41, 0.19], dtype=ftype)
    out_max = np.array([0.61, 0.61, 0.77, 0.77, 0.77], dtype=ftype)
    out_min = np.array([0.61, 0.60, 0.60, 0.41, 0.19], dtype=ftype)
    assert_equal(np.maximum.accumulate(arr), out_max)
    assert_equal(np.minimum.accumulate(arr), out_min)

