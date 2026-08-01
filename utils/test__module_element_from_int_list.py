
def test_ModuleElement_from_int_list():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    c = [1, 2, 3, 4]
    assert ModuleElement.from_int_list(A, c).coeffs == c

