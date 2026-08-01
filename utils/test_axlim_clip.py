
def test_axlim_clip(fig_test, fig_ref):
    # With axlim clipping
    ax = fig_test.add_subplot(projection="3d")
    x = np.linspace(0, 1, 11)
    y = np.linspace(0, 1, 11)
    X, Y = np.meshgrid(x, y)
    Z = X + Y
    ax.plot_surface(X, Y, Z, facecolor='C1', edgecolors=None,
                    rcount=50, ccount=50, axlim_clip=True)
    # This ax.plot is to cover the extra surface edge which is not clipped out
    ax.plot([0.5, 0.5], [0, 1], [0.5, 1.5],
            color='k', linewidth=3, zorder=5, axlim_clip=True)
    ax.scatter(X.ravel(), Y.ravel(), Z.ravel() + 1, axlim_clip=True)
    ax.quiver(X.ravel(), Y.ravel(), Z.ravel() + 2,
              0*X.ravel(), 0*Y.ravel(), 0*Z.ravel() + 1,
              arrow_length_ratio=0, axlim_clip=True)
    ax.plot(X[0], Y[0], Z[0] + 3, color='C2', axlim_clip=True)
    ax.text(1.1, 0.5, 4, 'test', axlim_clip=True)  # won't be visible
    ax.set(xlim=(0, 0.5), ylim=(0, 1), zlim=(0, 5))

    # With manual clipping
    ax = fig_ref.add_subplot(projection="3d")
    idx = (X <= 0.5)
    X = X[idx].reshape(11, 6)
    Y = Y[idx].reshape(11, 6)
    Z = Z[idx].reshape(11, 6)
    ax.plot_surface(X, Y, Z, facecolor='C1', edgecolors=None,
                    rcount=50, ccount=50, axlim_clip=False)
    ax.plot([0.5, 0.5], [0, 1], [0.5, 1.5],
            color='k', linewidth=3, zorder=5, axlim_clip=False)
    ax.scatter(X.ravel(), Y.ravel(), Z.ravel() + 1, axlim_clip=False)
    ax.quiver(X.ravel(), Y.ravel(), Z.ravel() + 2,
              0*X.ravel(), 0*Y.ravel(), 0*Z.ravel() + 1,
              arrow_length_ratio=0, axlim_clip=False)
    ax.plot(X[0], Y[0], Z[0] + 3, color='C2', axlim_clip=False)
    ax.set(xlim=(0, 0.5), ylim=(0, 1), zlim=(0, 5))

