
def draw_quiverkey_setzorder(fig, zorder=None):
    """Draw Quiver and QuiverKey using set_zorder"""
    x = np.arange(1, 6, 1)
    y = np.arange(1, 6, 1)
    X, Y = np.meshgrid(x, y)
    U, V = 2, 2

    ax = fig.subplots()
    q = ax.quiver(X, Y, U, V, pivot='middle')
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    qk1 = ax.quiverkey(q, 4, 4, 25, coordinates='data',
                       label='U', color='blue')
    qk2 = ax.quiverkey(q, 5.5, 2, 20, coordinates='data',
                       label='V', color='blue', angle=90)
    if zorder is not None:
        qk1.set_zorder(zorder)
        qk2.set_zorder(zorder)

