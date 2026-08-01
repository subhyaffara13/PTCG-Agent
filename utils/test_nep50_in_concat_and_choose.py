
def test_nep50_in_concat_and_choose():
    res = np.concatenate([np.float32(1), 1.], axis=None)
    assert res.dtype == "float32"

    res = np.choose(1, [np.float32(1), 1.])
    assert res.dtype == "float32"

