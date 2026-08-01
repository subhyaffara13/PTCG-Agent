
def test_axes3d_primary_views():
    # (elev, azim, roll)
    views = [(90, -90, 0),  # XY
             (0, -90, 0),   # XZ
             (0, 0, 0),     # YZ
             (-90, 90, 0),  # -XY
             (0, 90, 0),    # -XZ
             (0, 180, 0)]   # -YZ
    # When viewing primary planes, draw the two visible axes so they intersect
    # at their low values
    fig, axs = plt.subplots(2, 3, subplot_kw={'projection': '3d'})
    for i, ax in enumerate(axs.flat):
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_proj_type('ortho')
        ax.view_init(elev=views[i][0], azim=views[i][1], roll=views[i][2])
    plt.tight_layout()

