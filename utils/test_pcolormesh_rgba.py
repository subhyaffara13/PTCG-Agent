
def test_pcolormesh_rgba(fig_test, fig_ref, dims, alpha):
    ax = fig_test.subplots()
    c = np.ones((5, 6, dims), dtype=float) / 2
    ax.pcolormesh(c)

    ax = fig_ref.subplots()
    ax.pcolormesh(c[..., 0], cmap="gray", vmin=0, vmax=1, alpha=alpha)

