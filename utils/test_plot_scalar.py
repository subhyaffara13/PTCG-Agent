
def test_plot_scalar(fig_test, fig_ref):
    ax1 = fig_test.add_subplot(projection='3d')
    ax1.plot([1], [1], "o")
    ax2 = fig_ref.add_subplot(projection='3d')
    ax2.plot(1, 1, "o")

