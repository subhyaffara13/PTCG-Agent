
def test_qcut_bounds():
    arr = np.random.default_rng(2).standard_normal(1000)

    factor = qcut(arr, 10, labels=False)
    assert len(np.unique(factor)) == 10

