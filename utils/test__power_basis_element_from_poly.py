
def test_PowerBasis_element_from_poly():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    f = Poly(1 + 2*x)
    g = Poly(x**4)
    h = Poly(0, x)
    assert A.element_from_poly(f).coeffs == [1, 2, 0, 0]
    assert A.element_from_poly(g).coeffs == [-1, -1, -1, -1]
    assert A.element_from_poly(h).coeffs == [0, 0, 0, 0]

