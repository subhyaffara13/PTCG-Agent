
def test_index_using_ellipsis():
    a = m.index_using_ellipsis(np.zeros((5, 6, 7)))
    assert a.shape == (6,)

