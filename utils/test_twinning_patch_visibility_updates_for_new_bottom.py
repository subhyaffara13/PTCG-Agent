
def test_twinning_patch_visibility_updates_for_new_bottom():
    _, ax = plt.subplots()
    ax2 = ax.twinx()
    ax3 = ax.twinx(delta_zorder=-1)
    assert ax3.patch.get_visible()
    assert not ax2.patch.get_visible()
    assert not ax.patch.get_visible()

