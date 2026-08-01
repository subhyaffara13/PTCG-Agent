
def test_keyword_argument():
    # test for https://github.com/numpy/numpy/pull/16574#issuecomment-642660971
    assert np.dtype(dtype=np.float64) == np.dtype(np.float64)

