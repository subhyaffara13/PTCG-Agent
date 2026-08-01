
def test_lens_makers_formula_thick_lens():
    n1, n2 = symbols('n1, n2')
    m1 = Medium('m1', permittivity=e0, n=1)
    m2 = Medium('m2', permittivity=e0, n=1.33)
    assert ae(lens_makers_formula(m1, m2, 10, -10, d=1), -19.82, 2)
    assert lens_makers_formula(n1, n2, 1, -1, d=0.1) == n2/((2.0 - (0.1*n1 - 0.1*n2)/n1)*(n1 - n2))

