
def test_cosm1_opt():
    x = Symbol('x')

    expr1 = cos(x) - 1
    opt1 = optimize(expr1, [cosm1_opt])
    assert cosm1(x) - opt1 == 0
    assert opt1.rewrite(cos) == expr1

    expr2 = 3*cos(x) - 3
    opt2 = optimize(expr2, [cosm1_opt])
    assert 3*cosm1(x) == opt2
    assert opt2.rewrite(cos) == expr2

    expr3 = 3*cos(x) - 5
    opt3 = optimize(expr3, [cosm1_opt])
    assert 3*cosm1(x) - 2 == opt3
    assert opt3.rewrite(cos) == expr3
    cosm1_opt_non_opportunistic = FuncMinusOneOptim(cos, cosm1, opportunistic=False)
    assert expr3 == optimize(expr3, [cosm1_opt_non_opportunistic])
    assert opt1 == optimize(expr1, [cosm1_opt_non_opportunistic])
    assert opt2 == optimize(expr2, [cosm1_opt_non_opportunistic])

    expr4 = 3*cos(x) + log(x) - 3
    opt4 = optimize(expr4, [cosm1_opt])
    assert 3*cosm1(x) + log(x) == opt4
    assert opt4.rewrite(cos) == expr4

    expr5 = 3*cos(2*x) - 3
    opt5 = optimize(expr5, [cosm1_opt])
    assert 3*cosm1(2*x) == opt5
    assert opt5.rewrite(cos) == expr5

    expr6 = 2 - 2*cos(x)
    opt6 = optimize(expr6, [cosm1_opt])
    assert -2*cosm1(x) == opt6
    assert opt6.rewrite(cos) == expr6

