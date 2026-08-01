
def test_linecollection_scaled_dashes():
    lines1 = [[(0, .5), (.5, 1)], [(.3, .6), (.2, .2)]]
    lines2 = [[[0.7, .2], [.8, .4]], [[.5, .7], [.6, .1]]]
    lines3 = [[[0.6, .2], [.8, .4]], [[.5, .7], [.1, .1]]]
    lc1 = art3d.Line3DCollection(lines1, linestyles="--", lw=3)
    lc2 = art3d.Line3DCollection(lines2, linestyles="-.")
    lc3 = art3d.Line3DCollection(lines3, linestyles=":", lw=.5)

    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    ax.add_collection(lc1, autolim="_datalim_only")
    ax.add_collection(lc2, autolim="_datalim_only")
    ax.add_collection(lc3, autolim="_datalim_only")

    leg = ax.legend([lc1, lc2, lc3], ['line1', 'line2', 'line 3'])
    h1, h2, h3 = leg.legend_handles

    for oh, lh in zip((lc1, lc2, lc3), (h1, h2, h3)):
        assert oh.get_linestyles()[0] == lh._dash_pattern


def test_linecollection_scaled_dashes():
    lines1 = [[(0, .5), (.5, 1)], [(.3, .6), (.2, .2)]]
    lines2 = [[[0.7, .2], [.8, .4]], [[.5, .7], [.6, .1]]]
    lines3 = [[[0.6, .2], [.8, .4]], [[.5, .7], [.1, .1]]]
    lc1 = mcollections.LineCollection(lines1, linestyles="--", lw=3)
    lc2 = mcollections.LineCollection(lines2, linestyles="-.")
    lc3 = mcollections.LineCollection(lines3, linestyles=":", lw=.5)

    fig, ax = plt.subplots()
    ax.add_collection(lc1)
    ax.add_collection(lc2)
    ax.add_collection(lc3)

    leg = ax.legend([lc1, lc2, lc3], ["line1", "line2", 'line 3'])
    h1, h2, h3 = leg.legend_handles

    for oh, lh in zip((lc1, lc2, lc3), (h1, h2, h3)):
        assert oh.get_linestyles()[0] == lh._dash_pattern

