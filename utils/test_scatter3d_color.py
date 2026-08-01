
def test_scatter3d_color():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Check that 'none' color works; these two should overlay to produce the
    # same as setting just `color`.
    ax.scatter(np.arange(10), np.arange(10), np.arange(10),
               facecolor='r', edgecolor='none', marker='o')
    ax.scatter(np.arange(10), np.arange(10), np.arange(10),
               facecolor='none', edgecolor='r', marker='o')

    ax.scatter(np.arange(10, 20), np.arange(10, 20), np.arange(10, 20),
               color='b', marker='s')

