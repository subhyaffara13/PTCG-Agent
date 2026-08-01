
def test_set_rticks_ticklabels_no_warning():
    # Regression test: RadialLocator wrapping a FixedLocator must not trigger
    # the "set_ticklabels() should only be used with a fixed number of ticks"
    # UserWarning when set_ticks()/set_rticks() was called first.

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_rticks([0, 1, 2, 3])
    ax.yaxis.set_ticklabels(['zero', 'one', 'two', 'three'])

