
def test_remove_overlap(remove_overlapping_locs, expected_num):
    t = np.arange("2018-11-03", "2018-11-06", dtype="datetime64")
    x = np.ones(len(t))

    fig, ax = plt.subplots()
    ax.plot(t, x)

    ax.xaxis.set_major_locator(mpl.dates.DayLocator())
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('\n%a'))

    ax.xaxis.set_minor_locator(mpl.dates.HourLocator((0, 6, 12, 18)))
    ax.xaxis.set_minor_formatter(mpl.dates.DateFormatter('%H:%M'))
    # force there to be extra ticks
    ax.xaxis.get_minor_ticks(15)
    if remove_overlapping_locs is not None:
        ax.xaxis.remove_overlapping_locs = remove_overlapping_locs

    # check that getter/setter exists
    current = ax.xaxis.remove_overlapping_locs
    assert (current == ax.xaxis.get_remove_overlapping_locs())
    plt.setp(ax.xaxis, remove_overlapping_locs=current)
    new = ax.xaxis.remove_overlapping_locs
    assert (new == ax.xaxis.remove_overlapping_locs)

    # check that the accessors filter correctly
    # this is the method that does the actual filtering
    assert len(ax.xaxis.get_minorticklocs()) == expected_num
    # these three are derivative
    assert len(ax.xaxis.get_minor_ticks()) == expected_num
    assert len(ax.xaxis.get_minorticklabels()) == expected_num
    assert len(ax.xaxis.get_minorticklines()) == expected_num*2

