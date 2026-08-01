
def test_alt_transform():
    m1 = markers.MarkerStyle("o", "left")
    m2 = markers.MarkerStyle("o", "left", Affine2D().rotate_deg(90))
    assert m1.get_alt_transform().rotate_deg(90) == m2.get_alt_transform()

