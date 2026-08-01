
def test_deepcopy_0d_obj():
    source = np.ma.array(0, mask=[0], dtype=object)
    deepcopy = copy.deepcopy(source)
    deepcopy[...] = 17
    assert_equal(source, 0)
    assert_equal(deepcopy, 17)

