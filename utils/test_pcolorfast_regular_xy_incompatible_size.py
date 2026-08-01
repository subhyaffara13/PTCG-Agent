
def test_pcolorfast_regular_xy_incompatible_size():
    """
    Test that the sizes of X, Y, C are compatible for regularly spaced X, Y.

    Note that after the regualar-spacing check, pcolorfast may go into the
    fast "image" mode, where the individual X, Y positions are not used anymore.
    Therefore, the algorithm had worked with any regularly number of regularly
    spaced values, but discarded their values.
    """
    fig, ax = plt.subplots()
    with pytest.raises(
            ValueError, match=r"Length of X \(5\) must be one larger than the "
                              r"number of columns in C \(20\)"):
        ax.pcolorfast(np.arange(5), np.arange(11), np.random.rand(10, 20))

    with pytest.raises(
            ValueError, match=r"Length of Y \(5\) must be one larger than the "
                              r"number of rows in C \(10\)"):
        ax.pcolorfast(np.arange(21), np.arange(5), np.random.rand(10, 20))

