
def test_alpha_rcparam():
    fig, ax = plt.subplots()
    ax.plot(range(10), lw=5)
    with mpl.rc_context(rc={'legend.framealpha': .75}):
        leg = plt.legend(['Longlabel that will go away'], loc='center')
        # this alpha is going to be over-ridden by the rcparam with
        # sets the alpha of the patch to be non-None which causes the alpha
        # value of the face color to be discarded.  This behavior may not be
        # ideal, but it is what it is and we should keep track of it changing
        leg.legendPatch.set_facecolor([1, 0, 0, 0.5])

