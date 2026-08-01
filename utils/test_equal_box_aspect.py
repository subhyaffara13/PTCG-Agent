
def test_equal_box_aspect():
    from itertools import product, combinations

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # Make data
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))

    # Plot the surface
    ax.plot_surface(x, y, z)

    # draw cube
    r = [-1, 1]
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s - e)) == r[1] - r[0]:
            ax.plot3D(*zip(s, e), color="b")

    # Make axes limits
    xyzlim = np.column_stack(
        [ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()]
    )
    XYZlim = [min(xyzlim[0]), max(xyzlim[1])]
    ax.set_xlim3d(XYZlim)
    ax.set_ylim3d(XYZlim)
    ax.set_zlim3d(XYZlim)
    ax.axis('off')
    ax.set_box_aspect((1, 1, 1))

    with pytest.raises(ValueError, match="Argument zoom ="):
        ax.set_box_aspect((1, 1, 1), zoom=-1)

