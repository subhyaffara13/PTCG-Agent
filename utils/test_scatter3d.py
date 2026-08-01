
def test_scatter3d():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(np.arange(10), np.arange(10), np.arange(10),
               c='r', marker='o')
    x = y = z = np.arange(10, 20)
    ax.scatter(x, y, z, c='b', marker='^')
    z[-1] = 0  # Check that scatter() copies the data.
    # Ensure empty scatters do not break.
    ax.scatter([], [], [], c='r', marker='X')

