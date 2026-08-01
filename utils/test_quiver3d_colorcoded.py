
def test_quiver3d_colorcoded():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    x = y = dx = dz = np.zeros(10)
    z = dy = np.arange(10.)

    color = plt.colormaps["Reds"](dy/dy.max())
    ax.quiver(x, y, z, dx, dy, dz, colors=color)
    ax.set_ylim(0, 10)

