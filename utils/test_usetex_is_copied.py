
def test_usetex_is_copied():
    # Indirectly tests that update_from (which is used to copy tick label
    # properties) copies usetex state.
    fig = plt.figure()
    plt.rcParams["text.usetex"] = False
    ax1 = fig.add_subplot(121)
    plt.rcParams["text.usetex"] = True
    ax2 = fig.add_subplot(122)
    fig.canvas.draw()
    for ax, usetex in [(ax1, False), (ax2, True)]:
        for t in ax.xaxis.majorTicks:
            assert t.label1.get_usetex() == usetex

