
def test_hist():
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(['a', 'b', 'a', 'c', 'ff'])
    assert n.shape == (10,)
    np.testing.assert_allclose(n, [2., 0., 0., 1., 0., 0., 1., 0., 0., 1.])

