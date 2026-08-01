
def test_wireframe3dasymmetric():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X, Y, Z = axes3d.get_test_data(0.05)
    X, Y, Z = X[:-1], Y[:-1], Z[:-1]  # Drop a row so the grid is non-square
    ax.plot_wireframe(X, Y, Z, rcount=3, ccount=13)

