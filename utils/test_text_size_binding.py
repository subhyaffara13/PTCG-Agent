
def test_text_size_binding():
    mpl.rcParams['font.size'] = 10
    fp = mpl.font_manager.FontProperties(size='large')
    sz1 = fp.get_size_in_points()
    mpl.rcParams['font.size'] = 100

    assert sz1 == fp.get_size_in_points()

