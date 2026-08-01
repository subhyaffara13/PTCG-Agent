
def test_axvline_axvspan_do_not_modify_rlims():
    ax = plt.subplot(projection="polar")
    ax.axvspan(0, 1)
    ax.axvline(.5)
    ax.plot([.1, .2])
    assert ax.get_ylim() == (0, .2)

