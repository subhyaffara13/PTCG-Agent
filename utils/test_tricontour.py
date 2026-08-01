
def test_tricontour():
    plt.rcParams['axes3d.automargin'] = True  # Remove when image is regenerated
    fig = plt.figure()

    np.random.seed(19680801)
    x = np.random.rand(1000) - 0.5
    y = np.random.rand(1000) - 0.5
    z = -(x**2 + y**2)

    ax = fig.add_subplot(1, 2, 1, projection='3d')
    ax.tricontour(x, y, z)
    ax = fig.add_subplot(1, 2, 2, projection='3d')
    ax.tricontourf(x, y, z)

