
def test_scalar_for_scalar2():
    # test methods that are not attributes of frozen distributions
    res = stats.norm.fit([1, 2, 3])
    assert isinstance(res[0], np.number)
    assert isinstance(res[1], np.number)
    res = stats.norm.fit_loc_scale([1, 2, 3])
    assert isinstance(res[0], np.number)
    assert isinstance(res[1], np.number)
    res = stats.norm.nnlf((0, 1), [1, 2, 3])
    assert isinstance(res, np.number)

