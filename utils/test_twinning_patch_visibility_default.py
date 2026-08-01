
def test_twinning_patch_visibility_default():
    _, ax = plt.subplots()
    ax2 = ax.twinx()
    assert ax.patch.get_visible()
    assert not ax2.patch.get_visible()

