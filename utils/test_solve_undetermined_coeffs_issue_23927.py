
def test_solve_undetermined_coeffs_issue_23927():
    A, B, r, phi = symbols('A, B, r, phi')
    e = Eq(A*sin(t) + B*cos(t), r*sin(t - phi))
    eq = (e.lhs - e.rhs).expand(trig=True)
    soln = solve_undetermined_coeffs(eq, (r, phi), t)
    assert soln == [{
        phi: 2*atan((A - sqrt(A**2 + B**2))/B),
        r: (-A**2 + A*sqrt(A**2 + B**2) - B**2)/(A - sqrt(A**2 + B**2))
        }, {
        phi: 2*atan((A + sqrt(A**2 + B**2))/B),
        r: (A**2 + A*sqrt(A**2 + B**2) + B**2)/(A + sqrt(A**2 + B**2))/-1
        }]

