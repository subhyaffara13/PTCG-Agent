
def test_scatter_masked_color():
    """
    Test color parameter usage with non-finite coordinate arrays.

    GH#26236
    """

    x = [np.nan, 1, 2,  1]
    y = [0, np.inf, 2,  1]
    z = [0, 1, -np.inf, 1]
    colors = [
        [0.0, 0.0, 0.0, 1],
        [0.0, 0.0, 0.0, 1],
        [0.0, 0.0, 0.0, 1],
        [0.0, 0.0, 0.0, 1]
    ]

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    path3d = ax.scatter(x, y, z, color=colors)

    # Assert sizes' equality
    assert len(path3d.get_offsets()) ==\
           len(super(type(path3d), path3d).get_facecolors())

