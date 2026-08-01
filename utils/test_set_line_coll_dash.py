
def test_set_line_coll_dash():
    fig, ax = plt.subplots()
    np.random.seed(0)
    # Testing setting linestyles for line collections.
    # This should not produce an error.
    ax.contour(np.random.randn(20, 30), linestyles=[(0, (3, 3))])

