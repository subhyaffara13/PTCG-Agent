
def test_issue_17823():
    from sympy.physics.mechanics import dynamicsymbols
    q1, q2 = dynamicsymbols('q1, q2')
    expr = q1.diff().diff()**2*q1 + q1.diff()*q2.diff()
    reps={q1: a, q1.diff(): a*x*y, q1.diff().diff(): z}
    assert expr.subs(reps) == a*x*y*Derivative(q2, t) + a*z**2

