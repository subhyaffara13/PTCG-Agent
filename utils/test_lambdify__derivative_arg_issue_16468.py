
def test_lambdify_Derivative_arg_issue_16468():
    f = Function('f')(x)
    fx = f.diff()
    assert lambdify((f, fx), f + fx)(10, 5) == 15
    assert eval(lambdastr((f, fx), f/fx))(10, 5) == 2
    raises(Exception, lambda:
        eval(lambdastr((f, fx), f/fx, dummify=False)))
    assert eval(lambdastr((f, fx), f/fx, dummify=True))(10, 5) == 2
    assert eval(lambdastr((fx, f), f/fx, dummify=True))(S(10), 5) == S.Half
    assert lambdify(fx, 1 + fx)(41) == 42
    assert eval(lambdastr(fx, 1 + fx, dummify=True))(41) == 42

