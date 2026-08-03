import copy

def test_deepcopy_2d_obj():
    source = np.ma.array([[0, "dog"],
                          [1, 1],
                          [[1, 2], "cat"]],
                        mask=[[0, 1],
                              [0, 0],
                              [0, 0]],
                        dtype=object)
    deepcopy = copy.deepcopy(source)
    deepcopy[2, 0].extend(['this should not appear in source', 3])
    assert len(source[2, 0]) == 2
    assert len(deepcopy[2, 0]) == 4
    assert_equal(deepcopy._mask, source._mask)
    deepcopy._mask[0, 0] = 1
    assert source._mask[0, 0] == 0

