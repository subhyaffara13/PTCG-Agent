
def test_contour3d_1d_input():
    # Check that 1D sequences of different length for {x, y} doesn't error
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    nx, ny = 30, 20
    x = np.linspace(-10, 10, nx)
    y = np.linspace(-10, 10, ny)
    z = np.random.randint(0, 2, [ny, nx])
    ax.contour(x, y, z, [0.5])

