
def test_hexbin_log_offsets():
    x = np.geomspace(1, 100, 500)

    fig, ax = plt.subplots()
    h = ax.hexbin(x, x, xscale='log', yscale='log', gridsize=2)
    np.testing.assert_almost_equal(
        h.get_offsets(),
        np.array(
            [[0, 0],
             [0, 2],
             [1, 0],
             [1, 2],
             [2, 0],
             [2, 2],
             [0.5, 1],
             [1.5, 1]]))

