
def test_polar_gridlines():
    fig = plt.figure()
    ax = fig.add_subplot(polar=True)
    # make all major grid lines lighter, only x grid lines set in 2.1.0
    ax.grid(alpha=0.2)
    # hide y tick labels, no effect in 2.1.0
    plt.setp(ax.yaxis.get_ticklabels(), visible=False)
    fig.canvas.draw()
    assert ax.xaxis.majorTicks[0].gridline.get_alpha() == .2
    assert ax.yaxis.majorTicks[0].gridline.get_alpha() == .2

