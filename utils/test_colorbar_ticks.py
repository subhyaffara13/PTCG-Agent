
def test_colorbar_ticks():
    # test fix for #5673
    fig, ax = plt.subplots()
    x = np.arange(-3.0, 4.001)
    y = np.arange(-4.0, 3.001)
    X, Y = np.meshgrid(x, y)
    Z = X * Y
    clevs = np.array([-12, -5, 0, 5, 12], dtype=float)
    colors = ['r', 'g', 'b', 'c']
    cs = ax.contourf(X, Y, Z, clevs, colors=colors, extend='neither')
    cbar = fig.colorbar(cs, ax=ax, orientation='horizontal', ticks=clevs)
    assert len(cbar.ax.xaxis.get_ticklocs()) == len(clevs)

