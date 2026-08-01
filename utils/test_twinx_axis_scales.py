
def test_twinx_axis_scales():
    x = np.array([0, 0.5, 1])
    y = 0.5 * x
    x2 = np.array([0, 1, 2])
    y2 = 2 * x2

    fig = plt.figure()
    ax = fig.add_axes((0, 0, 1, 1), autoscalex_on=False, autoscaley_on=False)
    ax.plot(x, y, color='blue', lw=10)

    ax2 = plt.twinx(ax)
    ax2.plot(x2, y2, 'r--', lw=5)

    ax.margins(0, 0)
    ax2.margins(0, 0)

