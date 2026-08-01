
def test_startpoints():
    # Test varying startpoints. Also tests a non-default num_arrows argument.
    X, Y, U, V = velocity_field()
    start_x, start_y = np.meshgrid(np.linspace(X.min(), X.max(), 5),
                                   np.linspace(Y.min(), Y.max(), 5))
    start_points = np.column_stack([start_x.ravel(), start_y.ravel()])
    plt.streamplot(X, Y, U, V, start_points=start_points, num_arrows=4)
    plt.plot(start_x, start_y, 'ok')

