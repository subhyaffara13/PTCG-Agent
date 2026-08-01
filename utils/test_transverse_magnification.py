
def test_transverse_magnification():
    si, so = symbols('si, so')
    assert transverse_magnification(si, so) == -si/so
    assert transverse_magnification(30, 15) == -2

