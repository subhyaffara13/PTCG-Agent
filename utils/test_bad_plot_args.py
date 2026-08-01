
def test_bad_plot_args():
    with pytest.raises(ValueError):
        plt.plot(None)
    with pytest.raises(ValueError):
        plt.plot(None, None)
    with pytest.raises(ValueError):
        plt.plot(np.zeros((2, 2)), np.zeros((2, 3)))
    with pytest.raises(ValueError):
        plt.plot((np.arange(5).reshape((1, -1)), np.arange(5).reshape(-1, 1)))

