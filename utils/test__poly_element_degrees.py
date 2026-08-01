
def test_PolyElement_degrees():
    R, x,y,z = ring("x,y,z", ZZ)

    assert R(0).degrees() == (ninf, ninf, ninf)
    assert R(1).degrees() == (0, 0, 0)
    assert (x**2*y + x**3*z**2).degrees() == (3, 1, 2)

