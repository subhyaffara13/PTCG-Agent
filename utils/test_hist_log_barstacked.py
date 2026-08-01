
def test_hist_log_barstacked():
    fig, axs = plt.subplots(2)
    axs[0].hist([[0], [0, 1]], 2, histtype="barstacked")
    axs[0].set_yscale("log")
    axs[1].hist([0, 0, 1], 2, histtype="barstacked")
    axs[1].set_yscale("log")
    fig.canvas.draw()
    assert axs[0].get_ylim() == axs[1].get_ylim()

