
def test_pcolormesh_gouraud_nans():
    np.random.seed(19680801)

    values = np.linspace(0, 180, 3)
    radii = np.linspace(100, 1000, 10)
    z, y = np.meshgrid(values, radii)
    x = np.radians(np.random.rand(*z.shape) * 100)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="polar")
    # Setting the limit to cause clipping of the r values causes NaN to be
    # introduced; these should not crash but be ignored as in other path
    # operations.
    ax.set_rlim(101, 1000)
    ax.pcolormesh(x, y, z, shading="gouraud")

    fig.canvas.draw()

