
def test_issue_13143():
    f = Function('f')
    fx = f(x).diff(x)
    e = f(x) + fx + f(x)*fx
    # collect function before derivative
    assert collect(e, Wild('w')) == f(x)*(fx + 1) + fx
    e = f(x) + f(x)*fx + x*fx*f(x)
    assert collect(e, fx) == (x*f(x) + f(x))*fx + f(x)
    assert collect(e, f(x)) == (x*fx + fx + 1)*f(x)
    e = f(x) + fx + f(x)*fx
    assert collect(e, [f(x), fx]) == f(x)*(1 + fx) + fx
    assert collect(e, [fx, f(x)]) == fx*(1 + f(x)) + f(x)

