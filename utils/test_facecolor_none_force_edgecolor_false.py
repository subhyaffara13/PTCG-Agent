
def test_facecolor_none_force_edgecolor_false():
    rcParams['patch.force_edgecolor'] = False   # default value
    rect = Rectangle((0, 0), 1, 1, facecolor="none")
    assert rect.get_edgecolor() == (0.0, 0.0, 0.0, 0.0)

