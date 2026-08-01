
def test_suptitle_fontproperties():
    fig, ax = plt.subplots()
    fps = mpl.font_manager.FontProperties(size='large', weight='bold')
    txt = fig.suptitle('fontprops title', fontproperties=fps)
    assert txt.get_fontsize() == fps.get_size_in_points()
    assert txt.get_weight() == fps.get_weight()

