
def test_contourf3d_fill():
    plt.rcParams['axes3d.automargin'] = True  # Remove when image is regenerated
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X, Y = np.meshgrid(np.arange(-2, 2, 0.25), np.arange(-2, 2, 0.25))
    Z = X.clip(0, 0)
    # This produces holes in the z=0 surface that causes rendering errors if
    # the Poly3DCollection is not aware of path code information (issue #4784)
    Z[::5, ::5] = 0.1
    ax.contourf(X, Y, Z, offset=0, levels=[-0.1, 0], cmap="coolwarm")
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-1, 1)

