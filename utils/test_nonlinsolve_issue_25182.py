
def test_nonlinsolve_issue_25182():
    a1, b1, c1, ca, cb, cg = symbols('a1, b1, c1, ca, cb, cg')
    eq1 = a1*a1 + b1*b1 - 2.*a1*b1*cg - c1*c1
    eq2 = a1*a1 + c1*c1 - 2.*a1*c1*cb - b1*b1
    eq3 = b1*b1 + c1*c1 - 2.*b1*c1*ca - a1*a1
    assert nonlinsolve([eq1, eq2, eq3], [c1, cb, cg]) == FiniteSet(
        (1.0*b1*ca - 1.0*sqrt(a1**2 + b1**2*ca**2 - b1**2),
        -1.0*sqrt(a1**2 + b1**2*ca**2 - b1**2)/a1,
        -1.0*b1*(ca - 1)*(ca + 1)/a1 + 1.0*ca*sqrt(a1**2 + b1**2*ca**2 - b1**2)/a1),
        (1.0*b1*ca + 1.0*sqrt(a1**2 + b1**2*ca**2 - b1**2),
        1.0*sqrt(a1**2 + b1**2*ca**2 - b1**2)/a1,
        -1.0*b1*(ca - 1)*(ca + 1)/a1 - 1.0*ca*sqrt(a1**2 + b1**2*ca**2 - b1**2)/a1))

