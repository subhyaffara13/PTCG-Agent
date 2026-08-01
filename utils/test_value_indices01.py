
def test_value_indices01(xp):
    "Test dictionary keys and entries"
    data = xp.asarray([[1, 0, 0, 0, 0, 0],
                       [0, 0, 2, 2, 0, 0],
                       [0, 0, 2, 2, 2, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 4, 4, 0]])
    vi = ndimage.value_indices(data, ignore_value=0)
    true_keys = [1, 2, 4]
    assert list(vi.keys()) == true_keys

    truevi = {k: xp.nonzero(data == k) for k in true_keys}

    vi = ndimage.value_indices(data, ignore_value=0)
    assert vi.keys() == truevi.keys()
    for key in vi.keys():
        assert len(vi[key]) == len(truevi[key])
        for v, true_v in zip(vi[key], truevi[key]):
            xp_assert_equal(v, true_v)

