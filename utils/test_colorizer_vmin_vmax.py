
def test_colorizer_vmin_vmax():
    ca = mcolorizer.Colorizer()
    assert ca.vmin is None
    assert ca.vmax is None
    ca.vmin = 1
    ca.vmax = 3
    assert ca.vmin == 1.0
    assert ca.vmax == 3.0
    assert ca.norm.vmin == 1.0
    assert ca.norm.vmax == 3.0

