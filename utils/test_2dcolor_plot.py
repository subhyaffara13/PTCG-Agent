
def test_2dcolor_plot(fig_test, fig_ref):
    color = np.array([0.1, 0.2, 0.3])
    # plot with 1D-color:
    axs = fig_test.subplots(5)
    axs[0].plot([1, 2], [1, 2], c=color.reshape(-1))
    with pytest.warns(match="argument looks like a single numeric RGB"):
        axs[1].scatter([1, 2], [1, 2], c=color.reshape(-1))
    axs[2].step([1, 2], [1, 2], c=color.reshape(-1))
    axs[3].hist(np.arange(10), color=color.reshape(-1))
    axs[4].bar(np.arange(10), np.arange(10), color=color.reshape(-1))
    # plot with 2D-color:
    axs = fig_ref.subplots(5)
    axs[0].plot([1, 2], [1, 2], c=color.reshape((1, -1)))
    axs[1].scatter([1, 2], [1, 2], c=color.reshape((1, -1)))
    axs[2].step([1, 2], [1, 2], c=color.reshape((1, -1)))
    axs[3].hist(np.arange(10), color=color.reshape((1, -1)))
    axs[4].bar(np.arange(10), np.arange(10), color=color.reshape((1, -1)))

