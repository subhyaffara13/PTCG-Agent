
def test_plot_surface_None_arg(fig_test, fig_ref):
    x, y = np.meshgrid(np.arange(5), np.arange(5))
    z = x + y
    ax_test = fig_test.add_subplot(projection='3d')
    ax_test.plot_surface(x, y, z, facecolors=None)
    ax_ref = fig_ref.add_subplot(projection='3d')
    ax_ref.plot_surface(x, y, z)

