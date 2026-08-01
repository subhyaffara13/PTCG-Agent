
def test_Subplot():
    fig = plt.figure()

    ax = Subplot(fig, 1, 1, 1)
    fig.add_subplot(ax)

    xx = np.arange(0, 2 * np.pi, 0.01)
    ax.plot(xx, np.sin(xx))
    ax.set_ylabel("Test")

    ax.axis["left"].major_ticks.set_tick_out(False)
    ax.axis["right"].major_ticks.set_tick_out(False)

    ax.axis["bottom"].set_label("Tk0")

