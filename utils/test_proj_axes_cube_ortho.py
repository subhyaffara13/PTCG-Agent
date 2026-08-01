
def test_proj_axes_cube_ortho():
    E = np.array([200, 100, 100])
    R = np.array([0, 0, 0])
    V = np.array([0, 0, 1])
    roll = 0
    u, v, w = proj3d._view_axes(E, R, V, roll)
    viewM = proj3d._view_transformation_uvw(u, v, w, E)
    orthoM = proj3d._ortho_transformation(-1, 1)
    M = np.dot(orthoM, viewM)

    ts = '0 1 2 3 0 4 5 6 7 4'.split()
    xs = np.array([0, 1, 1, 0, 0, 0, 1, 1, 0, 0]) * 100
    ys = np.array([0, 0, 1, 1, 0, 0, 0, 1, 1, 0]) * 100
    zs = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1]) * 100

    txs, tys, tzs = proj3d.proj_transform(xs, ys, zs, M)

    fig, ax = _test_proj_draw_axes(M, s=150)

    ax.scatter(txs, tys, s=300-tzs)
    ax.plot(txs, tys, c='r')
    for x, y, t in zip(txs, tys, ts):
        ax.text(x, y, t)

    plt.rcParams['axes3d.automargin'] = True  # Remove when image is regenerated
    ax.set_xlim(-200, 200)
    ax.set_ylim(-200, 200)

