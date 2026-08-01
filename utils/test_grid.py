
def test_grid():
    fig, ax = plt.subplots()
    ax.grid()
    fig.canvas.draw()
    assert ax.xaxis.majorTicks[0].gridline.get_visible()
    ax.grid(visible=False)
    fig.canvas.draw()
    assert not ax.xaxis.majorTicks[0].gridline.get_visible()
    ax.grid(visible=True)
    fig.canvas.draw()
    assert ax.xaxis.majorTicks[0].gridline.get_visible()
    ax.grid()
    fig.canvas.draw()
    assert not ax.xaxis.majorTicks[0].gridline.get_visible()

