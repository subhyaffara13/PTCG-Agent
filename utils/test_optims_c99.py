
def test_optims_c99():
    x = Symbol('x')

    expr1 = 2**x + log(x)/log(2) + log(x + 1) + exp(x) - 1
    opt1 = optimize(expr1, optims_c99).simplify()
    assert opt1 == exp2(x) + log2(x) + log1p(x) + expm1(x)
    assert opt1.rewrite(exp).rewrite(log).rewrite(Pow) == expr1

    expr2 = log(x)/log(2) + log(x + 1)
    opt2 = optimize(expr2, optims_c99)
    assert opt2 == log2(x) + log1p(x)
    assert opt2.rewrite(log) == expr2

    expr3 = log(x)/log(2) + log(17*x + 17)
    opt3 = optimize(expr3, optims_c99)
    delta3 = opt3 - (log2(x) + log(17) + log1p(x))
    assert delta3 == 0
    assert (opt3.rewrite(log) - expr3).simplify() == 0

    expr4 = 2**x + 3*log(5*x + 7)/(13*log(2)) + 11*exp(x) - 11 + log(17*x + 17)
    opt4 = optimize(expr4, optims_c99).simplify()
    delta4 = opt4 - (exp2(x) + 3*log2(5*x + 7)/13 + 11*expm1(x) + log(17) + log1p(x))
    assert delta4 == 0
    assert (opt4.rewrite(exp).rewrite(log).rewrite(Pow) - expr4).simplify() == 0

    expr5 = 3*exp(2*x) - 3
    opt5 = optimize(expr5, optims_c99)
    delta5 = opt5 - 3*expm1(2*x)
    assert delta5 == 0
    assert opt5.rewrite(exp) == expr5

    expr6 = exp(2*x) - 3
    opt6 = optimize(expr6, optims_c99)
    assert opt6 in (expm1(2*x) - 2, expr6)  # expm1(2*x) - 2 is not better or worse

    expr7 = log(3*x + 3)
    opt7 = optimize(expr7, optims_c99)
    delta7 = opt7 - (log(3) + log1p(x))
    assert delta7 == 0
    assert (opt7.rewrite(log) - expr7).simplify() == 0

    expr8 = log(2*x + 3)
    opt8 = optimize(expr8, optims_c99)
    assert opt8 == expr8

