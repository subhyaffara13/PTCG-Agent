
def test_errorbar3d():
    """Tests limits, color styling, and legend for 3D errorbars."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    d = [1, 2, 3, 4, 5]
    e = [.5, .5, .5, .5, .5]
    ax.errorbar(x=d, y=d, z=d, xerr=e, yerr=e, zerr=e, capsize=3,
                zuplims=[False, True, False, True, True],
                zlolims=[True, False, False, True, False],
                yuplims=True,
                ecolor='purple', label='Error lines')
    ax.legend()

