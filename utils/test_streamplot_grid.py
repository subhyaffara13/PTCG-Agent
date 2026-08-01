
def test_streamplot_grid():
    u = np.ones((2, 2))
    v = np.zeros((2, 2))

    # Test for same rows and columns
    x = np.array([[10, 20], [10, 30]])
    y = np.array([[10, 10], [20, 20]])

    with pytest.raises(ValueError, match="The rows of 'x' must be equal"):
        plt.streamplot(x, y, u, v)

    x = np.array([[10, 20], [10, 20]])
    y = np.array([[10, 10], [20, 30]])

    with pytest.raises(ValueError, match="The columns of 'y' must be equal"):
        plt.streamplot(x, y, u, v)

    x = np.array([[10, 20], [10, 20]])
    y = np.array([[10, 10], [20, 20]])
    plt.streamplot(x, y, u, v)

    # Test for maximum dimensions
    x = np.array([0, 10])
    y = np.array([[[0, 10]]])

    with pytest.raises(ValueError, match="'y' can have at maximum "
                                         "2 dimensions"):
        plt.streamplot(x, y, u, v)

    # Test for equal spacing
    u = np.ones((3, 3))
    v = np.zeros((3, 3))
    x = np.array([0, 10, 20])
    y = np.array([0, 10, 30])

    with pytest.raises(ValueError, match="'y' values must be equally spaced"):
        plt.streamplot(x, y, u, v)

    # Test for strictly increasing
    x = np.array([0, 20, 40])
    y = np.array([0, 20, 10])

