
def test_transformation_to_pell():
    assert is_pell_transformation_ok(-13*x**2 - 7*x*y + y**2 + 2*x - 2*y - 14)
    assert is_pell_transformation_ok(-17*x**2 + 19*x*y - 7*y**2 - 5*x - 13*y - 23)
    assert is_pell_transformation_ok(x**2 - y**2 + 17)
    assert is_pell_transformation_ok(-x**2 + 7*y**2 - 23)
    assert is_pell_transformation_ok(25*x**2 - 45*x*y + 5*y**2 - 5*x - 10*y + 5)
    assert is_pell_transformation_ok(190*x**2 + 30*x*y + y**2 - 3*y - 170*x - 130)
    assert is_pell_transformation_ok(x**2 - 2*x*y -190*y**2 - 7*y - 23*x - 89)
    assert is_pell_transformation_ok(15*x**2 - 9*x*y + 14*y**2 - 23*x - 14*y - 4950)

