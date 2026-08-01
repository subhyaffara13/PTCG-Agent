
def test_is_groebner():
    R, x,y = ring("x,y", QQ, grlex)
    valid_groebner = [x**2, x*y, -QQ(1,2)*x + y**2]
    invalid_groebner = [x**3, x*y, -QQ(1,2)*x + y**2]
    assert is_groebner(valid_groebner, R) is True
    assert is_groebner(invalid_groebner, R) is False

