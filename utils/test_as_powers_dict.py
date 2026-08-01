
def test_as_powers_dict():
    assert x.as_powers_dict() == {x: 1}
    assert (x**y*z).as_powers_dict() == {x: y, z: 1}
    assert Mul(2, 2, evaluate=False).as_powers_dict() == {S(2): S(2)}
    assert (x*y).as_powers_dict()[z] == 0
    assert (x + y).as_powers_dict()[z] == 0

