
def test_Poly_total_degree():
    assert Poly(x**2*y + x**3*z**2 + 1).total_degree() == 5
    assert Poly(x**2 + z**3).total_degree() == 3
    assert Poly(x*y*z + z**4).total_degree() == 4
    assert Poly(x**3 + x + 1).total_degree() == 3

    assert total_degree(x*y + z**3) == 3
    assert total_degree(x*y + z**3, x, y) == 2
    assert total_degree(1) == 0
    assert total_degree(Poly(y**2 + x**3 + z**4)) == 4
    assert total_degree(Poly(y**2 + x**3 + z**4, x)) == 3
    assert total_degree(Poly(y**2 + x**3 + z**4, x), z) == 4
    assert total_degree(Poly(x**9 + x*z*y + x**3*z**2 + z**7,x), z) == 7

