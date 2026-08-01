
def test_proj_axes_cube():
    M = _test_proj_make_M()

    ts = '0 1 2 3 0 4 5 6 7 4'.split()
    xs = np.array([0, 1, 1, 0, 0, 0, 1, 1, 0, 0]) * 300.0
    ys = np.array([0, 0, 1, 1, 0, 0, 0, 1, 1, 0]) * 300.0
    zs = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1]) * 300.0

    txs, tys, tzs = proj3d.proj_transform(xs, ys, zs, M)

    fig, ax = _test_proj_draw_axes(M, s=400)

    ax.scatter(txs, tys, c=tzs)
    ax.plot(txs, tys, c='r')
    for x, y, t in zip(txs, tys, ts):
        ax.text(x, y, t)

    plt.rcParams['axes3d.automargin'] = True  # Remove when image is regenerated
    ax.set_xlim(-0.2, 0.2)
    ax.set_ylim(-0.2, 0.2)

