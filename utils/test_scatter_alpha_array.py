
def test_scatter_alpha_array():
    x = np.arange(5)
    alpha = x / 5
    # With colormapping.
    fig, (ax0, ax1) = plt.subplots(2)
    sc0 = ax0.scatter(x, x, c=x, alpha=alpha)
    sc1 = ax1.scatter(x, x, c=x)
    sc1.set_alpha(alpha)
    plt.draw()
    assert_array_equal(sc0.get_facecolors()[:, -1], alpha)
    assert_array_equal(sc1.get_facecolors()[:, -1], alpha)
    # Without colormapping.
    fig, (ax0, ax1) = plt.subplots(2)
    sc0 = ax0.scatter(x, x, color=['r', 'g', 'b', 'c', 'm'], alpha=alpha)
    sc1 = ax1.scatter(x, x, color='r', alpha=alpha)
    plt.draw()
    assert_array_equal(sc0.get_facecolors()[:, -1], alpha)
    assert_array_equal(sc1.get_facecolors()[:, -1], alpha)
    # Without colormapping, and set alpha afterward.
    fig, (ax0, ax1) = plt.subplots(2)
    sc0 = ax0.scatter(x, x, color=['r', 'g', 'b', 'c', 'm'])
    sc0.set_alpha(alpha)
    sc1 = ax1.scatter(x, x, color='r')
    sc1.set_alpha(alpha)
    plt.draw()
    assert_array_equal(sc0.get_facecolors()[:, -1], alpha)
    assert_array_equal(sc1.get_facecolors()[:, -1], alpha)

