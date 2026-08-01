
def test_axes_removal():
    # Check that units can set the formatter after an Axes removal
    fig, axs = plt.subplots(1, 2, sharex=True)
    axs[1].remove()
    axs[0].plot([datetime(2000, 1, 1), datetime(2000, 2, 1)], [0, 1])
    assert isinstance(axs[0].xaxis.get_major_formatter(),
                      mdates.AutoDateFormatter)

    # Check that manually setting the formatter, then removing Axes keeps
    # the set formatter.
    fig, axs = plt.subplots(1, 2, sharex=True)
    axs[1].xaxis.set_major_formatter(ScalarFormatter())
    axs[1].remove()
    axs[0].plot([datetime(2000, 1, 1), datetime(2000, 2, 1)], [0, 1])
    assert isinstance(axs[0].xaxis.get_major_formatter(),
                      ScalarFormatter)

