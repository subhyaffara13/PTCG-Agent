
def test_marker_cycle():
    fig, ax = plt.subplots()
    ax.set_prop_cycle(cycler('c', ['r', 'g', 'y']) +
                      cycler('marker', ['.', '*', 'x']))
    for _ in range(4):
        ax.plot(range(10), range(10))
    assert [l.get_color() for l in ax.lines] == ['r', 'g', 'y', 'r']
    assert [l.get_marker() for l in ax.lines] == ['.', '*', 'x', '.']

