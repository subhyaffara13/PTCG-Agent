
def test_surface3d_masked():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    y = [1, 2, 3, 4, 5, 6, 7, 8]

    x, y = np.meshgrid(x, y)
    matrix = np.array(
        [
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-1, 1, 2, 3, 4, 4, 4, 3, 2, 1, 1],
            [-1, -1., 4, 5, 6, 8, 6, 5, 4, 3, -1.],
            [-1, -1., 7, 8, 11, 12, 11, 8, 7, -1., -1.],
            [-1, -1., 8, 9, 10, 16, 10, 9, 10, 7, -1.],
            [-1, -1., -1., 12, 16, 20, 16, 12, 11, -1., -1.],
            [-1, -1., -1., -1., 22, 24, 22, 20, 18, -1., -1.],
            [-1, -1., -1., -1., -1., 28, 26, 25, -1., -1., -1.],
        ]
    )
    z = np.ma.masked_less(matrix, 0)
    norm = mcolors.Normalize(vmax=z.max(), vmin=z.min())
    colors = mpl.colormaps["plasma"](norm(z))
    ax.plot_surface(x, y, z, facecolors=colors)
    ax.view_init(30, -80, 0)

