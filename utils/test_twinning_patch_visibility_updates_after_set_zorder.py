
def test_twinning_patch_visibility_updates_after_set_zorder():
    _, ax = plt.subplots()
    ax2 = ax.twinx()
    assert ax.patch.get_visible()
    assert not ax2.patch.get_visible()

    ax2.set_zorder(ax.get_zorder() - 1)
    assert ax2.patch.get_visible()
    assert not ax.patch.get_visible()

