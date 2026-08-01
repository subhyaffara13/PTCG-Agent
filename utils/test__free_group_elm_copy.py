
def test_FreeGroupElm_copy():
    f = x*y*z**3
    g = f.copy()
    h = x*y*z**7

    assert f == g
    assert f != h

