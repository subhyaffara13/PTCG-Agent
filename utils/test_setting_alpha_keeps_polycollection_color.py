
def test_setting_alpha_keeps_polycollection_color():
    pc = plt.fill_between([0, 1], [2, 3], color='#123456', label='label')
    patch = plt.legend().get_patches()[0]
    patch.set_alpha(0.5)
    assert patch.get_facecolor()[:3] == tuple(pc.get_facecolor()[0][:3])
    assert patch.get_edgecolor()[:3] == tuple(pc.get_edgecolor()[0][:3])

