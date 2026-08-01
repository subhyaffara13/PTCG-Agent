
def test_reused_gridspec():
    """Test that these all use the same gridspec"""
    fig = plt.figure()
    ax1 = fig.add_subplot(3, 2, (3, 5))
    ax2 = fig.add_subplot(3, 2, 4)
    ax3 = plt.subplot2grid((3, 2), (2, 1), colspan=2, fig=fig)

    gs1 = ax1.get_subplotspec().get_gridspec()
    gs2 = ax2.get_subplotspec().get_gridspec()
    gs3 = ax3.get_subplotspec().get_gridspec()

    assert gs1 == gs2
    assert gs1 == gs3

