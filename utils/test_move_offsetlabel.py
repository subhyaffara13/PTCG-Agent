
def test_move_offsetlabel():
    data = np.random.random(10) * 1e-22

    fig, ax = plt.subplots()
    ax.plot(data)
    fig.canvas.draw()
    before = ax.yaxis.offsetText.get_position()
    assert ax.yaxis.offsetText.get_horizontalalignment() == 'left'
    ax.yaxis.tick_right()
    fig.canvas.draw()
    after = ax.yaxis.offsetText.get_position()
    assert after[0] > before[0] and after[1] == before[1]
    assert ax.yaxis.offsetText.get_horizontalalignment() == 'right'

    fig, ax = plt.subplots()
    ax.plot(data)
    fig.canvas.draw()
    before = ax.xaxis.offsetText.get_position()
    assert ax.xaxis.offsetText.get_verticalalignment() == 'top'
    ax.xaxis.tick_top()
    fig.canvas.draw()
    after = ax.xaxis.offsetText.get_position()
    assert after[0] == before[0] and after[1] > before[1]
    assert ax.xaxis.offsetText.get_verticalalignment() == 'bottom'

