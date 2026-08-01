
def test_lens_makers_formula_plano_lens():
    n1, n2 = symbols('n1, n2')
    m1 = Medium('m1', permittivity=e0, n=1)
    m2 = Medium('m2', permittivity=e0, n=1.33)
    assert ae(lens_makers_formula(m1, m2, 10, oo), -40.30, 2)
    assert lens_makers_formula(n1, n2, 10, oo) == 10.0*n2/(n1 - n2)

