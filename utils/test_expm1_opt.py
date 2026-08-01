
def test_expm1_opt():
    x = Symbol('x')

    expr1 = exp(x) - 1
    opt1 = optimize(expr1, [expm1_opt])
    assert expm1(x) - opt1 == 0
    assert opt1.rewrite(exp) == expr1

    expr2 = 3*exp(x) - 3
    opt2 = optimize(expr2, [expm1_opt])
    assert 3*expm1(x) == opt2
    assert opt2.rewrite(exp) == expr2

    expr3 = 3*exp(x) - 5
    opt3 = optimize(expr3, [expm1_opt])
    assert 3*expm1(x) - 2 == opt3
    assert opt3.rewrite(exp) == expr3
    expm1_opt_non_opportunistic = FuncMinusOneOptim(exp, expm1, opportunistic=False)
    assert expr3 == optimize(expr3, [expm1_opt_non_opportunistic])
    assert opt1 == optimize(expr1, [expm1_opt_non_opportunistic])
    assert opt2 == optimize(expr2, [expm1_opt_non_opportunistic])

    expr4 = 3*exp(x) + log(x) - 3
    opt4 = optimize(expr4, [expm1_opt])
    assert 3*expm1(x) + log(x) == opt4
    assert opt4.rewrite(exp) == expr4

    expr5 = 3*exp(2*x) - 3
    opt5 = optimize(expr5, [expm1_opt])
    assert 3*expm1(2*x) == opt5
    assert opt5.rewrite(exp) == expr5

    expr6 = (2*exp(x) + 1)/(exp(x) + 1) + 1
    opt6 = optimize(expr6, [expm1_opt])
    assert opt6.count_ops() <= expr6.count_ops()

    def ev(e):
        return e.subs(x, 3).evalf()
    assert abs(ev(expr6) - ev(opt6)) < 1e-15

    y = Symbol('y')
    expr7 = (2*exp(x) - 1)/(1 - exp(y)) - 1/(1-exp(y))
    opt7 = optimize(expr7, [expm1_opt])
    assert -2*expm1(x)/expm1(y) == opt7
    assert (opt7.rewrite(exp) - expr7).factor() == 0

    expr8 = (1+exp(x))**2 - 4
    opt8 = optimize(expr8, [expm1_opt])
    tgt8a = (exp(x) + 3)*expm1(x)
    tgt8b = 2*expm1(x) + expm1(2*x)
    # Both tgt8a & tgt8b seem to give full precision (~16 digits for double)
    # for x=1e-7 (compare with expr8 which only achieves ~8 significant digits).
    # If we can show that either tgt8a or tgt8b is preferable, we can
    # change this test to ensure the preferable version is returned.
    assert (tgt8a - tgt8b).rewrite(exp).factor() == 0
    assert opt8 in (tgt8a, tgt8b)
    assert (opt8.rewrite(exp) - expr8).factor() == 0

    expr9 = sin(expr8)
    opt9 = optimize(expr9, [expm1_opt])
    tgt9a = sin(tgt8a)
    tgt9b = sin(tgt8b)
    assert opt9 in (tgt9a, tgt9b)
    assert (opt9.rewrite(exp) - expr9.rewrite(exp)).factor().is_zero

