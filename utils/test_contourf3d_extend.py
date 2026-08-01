
def test_contourf3d_extend(fig_test, fig_ref, extend, levels):
    X, Y = np.meshgrid(np.arange(-2, 2, 0.25), np.arange(-2, 2, 0.25))
    # Z is in the range [0, 8]
    Z = X**2 + Y**2

    ax_ref = fig_ref.add_subplot(projection='3d')
    ax_ref.contourf(X, Y, Z, levels=[0, 2, 4, 6, 8], vmin=1, vmax=7)

    ax_test = fig_test.add_subplot(projection='3d')
    ax_test.contourf(X, Y, Z, levels, extend=extend, vmin=1, vmax=7)

    for ax in [ax_ref, ax_test]:
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_zlim(-10, 10)

