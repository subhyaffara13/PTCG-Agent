
def test_gh_22556():
    source = np.ma.array([0, [0, 1, 2]], dtype=object)
    deepcopy = copy.deepcopy(source)
    deepcopy[1].append('this should not appear in source')
    assert len(source[1]) == 3

