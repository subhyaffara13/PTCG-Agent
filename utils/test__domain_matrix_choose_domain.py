
def test_DomainMatrix_choose_domain():
    A = [[1, 2], [3, 0]]
    assert DM(A, QQ).choose_domain() == DM(A, ZZ)
    assert DM(A, QQ).choose_domain(field=True) == DM(A, QQ)
    assert DM(A, ZZ).choose_domain(field=True) == DM(A, QQ)

    x = symbols('x')
    B = [[1, x], [x**2, x**3]]
    assert DM(B, QQ[x]).choose_domain(field=True) == DM(B, ZZ.frac_field(x))

