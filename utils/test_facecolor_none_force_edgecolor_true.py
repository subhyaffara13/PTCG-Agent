
def test_facecolor_none_force_edgecolor_true():
    rcParams['patch.force_edgecolor'] = True
    rect = Rectangle((0, 0), 1, 1, facecolor="none")
    assert rect.get_edgecolor() == (0.0, 0.0, 0.0, 1)

