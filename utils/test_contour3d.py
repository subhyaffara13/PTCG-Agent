
def test_contour3d():
    plt.rcParams['axes3d.automargin'] = True  # Remove when image is regenerated
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X, Y, Z = axes3d.get_test_data(0.05)
    ax.contour(X, Y, Z, zdir='z', offset=-100, cmap="coolwarm")
    ax.contour(X, Y, Z, zdir='x', offset=-40, cmap="coolwarm")
    ax.contour(X, Y, Z, zdir='y', offset=40, cmap="coolwarm")
    ax.axis(xmin=-40, xmax=40, ymin=-40, ymax=40, zmin=-100, zmax=100)

