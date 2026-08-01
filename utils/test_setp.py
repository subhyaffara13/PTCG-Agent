
def test_setp():
    # Check empty list
    plt.setp([])
    plt.setp([[]])

    # Check arbitrary iterables
    fig, ax = plt.subplots()
    lines1 = ax.plot(range(3))
    lines2 = ax.plot(range(3))
    martist.setp(chain(lines1, lines2), 'lw', 5)
    plt.setp(ax.spines.values(), color='green')

    # Check *file* argument
    sio = io.StringIO()
    plt.setp(lines1, 'zorder', file=sio)
    assert sio.getvalue() == '  zorder: float\n'

