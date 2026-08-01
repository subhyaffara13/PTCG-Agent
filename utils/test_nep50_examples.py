
def test_nep50_examples():
    res = np.uint8(1) + 2
    assert res.dtype == np.uint8

    res = np.array([1], np.uint8) + np.int64(1)
    assert res.dtype == np.int64

    res = np.array([1], np.uint8) + np.array(1, dtype=np.int64)
    assert res.dtype == np.int64

    with pytest.warns(RuntimeWarning, match="overflow"):
        res = np.uint8(100) + 200
    assert res.dtype == np.uint8

    with pytest.warns(RuntimeWarning, match="overflow"):
        res = np.float32(1) + 3e100

    assert np.isinf(res)
    assert res.dtype == np.float32

    res = np.array([0.1], np.float32) == np.float64(0.1)
    assert res[0] == False

    res = np.array([0.1], np.float32) + np.float64(0.1)
    assert res.dtype == np.float64

    res = np.array([1.], np.float32) + np.int64(3)
    assert res.dtype == np.float64

