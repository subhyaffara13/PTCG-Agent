
def test_outer_exceeds_maxdims():
    deep = np.ones((1,) * 33)
    with assert_raises(ValueError):
        np.add.outer(deep, deep)

