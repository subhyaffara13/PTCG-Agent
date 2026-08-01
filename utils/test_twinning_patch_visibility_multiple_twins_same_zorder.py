
def test_twinning_patch_visibility_multiple_twins_same_zorder():
    _, ax = plt.subplots()
    ax2 = ax.twinx()
    ax3 = ax.twinx()
    assert ax.patch.get_visible()
    assert not ax2.patch.get_visible()
    assert not ax3.patch.get_visible()

