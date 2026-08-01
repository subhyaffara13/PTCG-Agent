
def test_twinning_patch_visibility_respects_delta_zorder():
    _, ax = plt.subplots()
    ax2 = ax.twinx(delta_zorder=-1)
    assert ax2.get_zorder() == ax.get_zorder() - 1
    assert ax2.patch.get_visible()
    assert not ax.patch.get_visible()

