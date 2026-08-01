
def test_ax3d_tickcolour():
    fig = plt.figure()
    ax = Axes3D(fig)

    ax.tick_params(axis='x', colors='red')
    ax.tick_params(axis='y', colors='red')
    ax.tick_params(axis='z', colors='red')
    fig.canvas.draw()

    for tick in ax.xaxis.get_major_ticks():
        assert tick.tick1line._color == 'red'
    for tick in ax.yaxis.get_major_ticks():
        assert tick.tick1line._color == 'red'
    for tick in ax.zaxis.get_major_ticks():
        assert tick.tick1line._color == 'red'

