
def test_PolyElement_gff_list():
    _, x = ring("x", ZZ)

    f = x**5 + 2*x**4 - x**3 - 2*x**2
    assert f.gff_list() == [(x, 1), (x + 2, 4)]

    f = x*(x - 1)**3*(x - 2)**2*(x - 4)**2*(x - 5)
    assert f.gff_list() == [(x**2 - 5*x + 4, 1), (x**2 - 5*x + 4, 2), (x, 3)]

