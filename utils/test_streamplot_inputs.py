
def test_streamplot_inputs():  # test no exception occurs.
    # fully-masked
    plt.streamplot(np.arange(3), np.arange(3),
                   np.full((3, 3), np.nan), np.full((3, 3), np.nan),
                   color=np.random.rand(3, 3))
    # array-likes
    plt.streamplot(range(3), range(3),
                   np.random.rand(3, 3), np.random.rand(3, 3))

