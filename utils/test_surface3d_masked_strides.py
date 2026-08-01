
def test_surface3d_masked_strides():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    x, y = np.mgrid[-6:6.1:1, -6:6.1:1]
    z = np.ma.masked_less(x * y, 2)

    ax.plot_surface(x, y, z, rstride=4, cstride=4)
    ax.view_init(60, -45, 0)

