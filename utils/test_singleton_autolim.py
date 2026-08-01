
def test_singleton_autolim():
    fig, ax = plt.subplots()
    ax.scatter(0, 0)
    np.testing.assert_allclose(ax.get_ylim(), [-0.06, 0.06])
    np.testing.assert_allclose(ax.get_xlim(), [-0.06, 0.06])

