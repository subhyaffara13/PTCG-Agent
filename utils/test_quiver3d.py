
def test_quiver3d():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    pivots = ['tip', 'middle', 'tail']
    colors = ['tab:blue', 'tab:orange', 'tab:green']
    for i, (pivot, color) in enumerate(zip(pivots, colors)):
        x, y, z = np.meshgrid([-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5])
        u = -x
        v = -y
        w = -z
        # Offset each set in z direction
        z += 2 * i
        ax.quiver(x, y, z, u, v, w, length=1, pivot=pivot, color=color)
        ax.scatter(x, y, z, color=color)

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-1, 5)

