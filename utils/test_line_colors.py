
def test_line_colors():
    fig, ax = plt.subplots()
    ax.plot(range(10), color='none')
    ax.plot(range(10), color='r')
    ax.plot(range(10), color='.3')
    ax.plot(range(10), color=(1, 0, 0, 1))
    ax.plot(range(10), color=(1, 0, 0))
    fig.canvas.draw()

