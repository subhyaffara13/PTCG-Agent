
def test_lens_makers_formula():
    n1, n2 = symbols('n1, n2')
    m1 = Medium('m1', permittivity=e0, n=1)
    m2 = Medium('m2', permittivity=e0, n=1.33)
    assert lens_makers_formula(n1, n2, 10, -10) == 5.0*n2/(n1 - n2)
    assert ae(lens_makers_formula(m1, m2, 10, -10), -20.15, 2)
    assert ae(lens_makers_formula(1.33, 1, 10, -10),  15.15, 2)

