
def test_colorbar_single_ax_panchor_false():
    # Note that this differs from the tests above with panchor=False because
    # there use_gridspec is actually ineffective: passing *ax* as lists always
    # disables use_gridspec.
    ax = plt.subplot(111, anchor='N')
    plt.imshow([[0, 1]])
    plt.colorbar(panchor=False)
    assert ax.get_anchor() == 'N'

