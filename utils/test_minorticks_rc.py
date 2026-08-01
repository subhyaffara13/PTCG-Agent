
def test_minorticks_rc():
    fig = plt.figure()

    def minorticksubplot(xminor, yminor, i):
        rc = {'xtick.minor.visible': xminor,
              'ytick.minor.visible': yminor}
        with plt.rc_context(rc=rc):
            ax = fig.add_subplot(2, 2, i)

        assert (len(ax.xaxis.get_minor_ticks()) > 0) == xminor
        assert (len(ax.yaxis.get_minor_ticks()) > 0) == yminor

    minorticksubplot(False, False, 1)
    minorticksubplot(True, False, 2)
    minorticksubplot(False, True, 3)
    minorticksubplot(True, True, 4)

