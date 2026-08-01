
def draw_quiverkey_zorder_argument(fig, zorder=None):
    """Draw Quiver and QuiverKey using zorder argument"""
    x = np.arange(1, 6, 1)
    y = np.arange(1, 6, 1)
    X, Y = np.meshgrid(x, y)
    U, V = 2, 2

    ax = fig.subplots()
    q = ax.quiver(X, Y, U, V, pivot='middle')
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    if zorder is None:
        ax.quiverkey(q, 4, 4, 25, coordinates='data',
                     label='U', color='blue')
        ax.quiverkey(q, 5.5, 2, 20, coordinates='data',
                     label='V', color='blue', angle=90)
    else:
        ax.quiverkey(q, 4, 4, 25, coordinates='data',
                     label='U', color='blue', zorder=zorder)
        ax.quiverkey(q, 5.5, 2, 20, coordinates='data',
                     label='V', color='blue', angle=90, zorder=zorder)

