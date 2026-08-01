
def test_errorbar3d_errorevery():
    """Tests errorevery functionality for 3D errorbars."""
    t = np.arange(0, 2*np.pi+.1, 0.01)
    x, y, z = np.sin(t), np.cos(3*t), np.sin(5*t)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    estep = 15
    i = np.arange(t.size)
    zuplims = (i % estep == 0) & (i // estep % 3 == 0)
    zlolims = (i % estep == 0) & (i // estep % 3 == 2)

    ax.errorbar(x, y, z, 0.2, zuplims=zuplims, zlolims=zlolims,
                errorevery=estep)

