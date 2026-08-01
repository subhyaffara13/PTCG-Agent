
def test_fillcycle_ignore():
    fig, ax = plt.subplots()
    ax.set_prop_cycle(cycler('color',  ['r', 'g', 'y']) +
                      cycler('hatch', ['xx', 'O', '|-']) +
                      cycler('marker', ['.', '*', 'D']))
    t = range(10)
    # Should not advance the cycler, even though there is an
    # unspecified property in the cycler "marker".
    # "marker" is not a Polygon property, and should be ignored.
    ax.fill(t, t, 'r', hatch='xx')
    # Allow the cycler to advance, but specify some properties
    ax.fill(t, t, hatch='O')
    ax.fill(t, t)
    ax.fill(t, t)
    assert ([p.get_facecolor() for p in ax.patches]
            == [mpl.colors.to_rgba(c) for c in ['r', 'r', 'g', 'y']])
    assert [p.get_hatch() for p in ax.patches] == ['xx', 'O', 'O', '|-']

