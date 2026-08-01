
def test_PolyElement_tail_degrees():
    R, x,y,z = ring("x,y,z", ZZ)

    assert R(0).tail_degrees() == (ninf, ninf, ninf)
    assert R(1).tail_degrees() == (0, 0, 0)
    assert (x**2*y + x**3*z**2).tail_degrees() == (2, 0, 0)

