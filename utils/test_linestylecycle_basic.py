
def test_linestylecycle_basic():
    fig, ax = plt.subplots()
    ax.set_prop_cycle(cycler('ls', ['-', '--', ':']))
    for _ in range(4):
        ax.plot(range(10), range(10))
    assert [l.get_linestyle() for l in ax.lines] == ['-', '--', ':', '-']

