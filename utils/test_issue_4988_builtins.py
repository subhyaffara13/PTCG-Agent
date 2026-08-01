
def test_issue_4988_builtins():
    C = Symbol('C')
    vars = {'C': C}
    exp1 = sympify('C')
    assert exp1 == C  # Make sure it did not get mixed up with sympy.C

    exp2 = sympify('C', vars)
    assert exp2 == C  # Make sure it did not get mixed up with sympy.C

