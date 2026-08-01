
def test_ModuleElement_reduced_mod_p():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    e = A(to_col([20, 40, 60, 80]))
    f = e.reduced_mod_p(7)
    assert f.coeffs == [-1, -2, -3, 3]

