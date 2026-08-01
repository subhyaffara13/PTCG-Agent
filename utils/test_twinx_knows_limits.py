
def test_twinx_knows_limits():
    fig, ax = plt.subplots()

    ax.axvspan(1, 2)
    xtwin = ax.twinx()
    xtwin.plot([0, 0.5], [1, 2])
    # control axis
    fig2, ax2 = plt.subplots()

    ax2.axvspan(1, 2)
    ax2.plot([0, 0.5], [1, 2])

    assert_array_equal(xtwin.viewLim.intervalx, ax2.viewLim.intervalx)

