
def test_FracElement_evaluate():
    F, x,y,z = field("x,y,z", ZZ)
    Fyz = field("y,z", ZZ)[0]
    f = (x**2 + 3*y)/z

    assert f.evaluate(x, 0) == 3*Fyz.y/Fyz.z
    raises(ZeroDivisionError, lambda: f.evaluate(z, 0))

