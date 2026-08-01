
def test_issue_20782():
    fun1 = Piecewise((0, x < 0.0), (1, True))
    fun2 = -Piecewise((0, x < 1.0), (1, True))
    fun_sum = fun1 + fun2
    L = (x, -float('Inf'), 1)

    assert integrate(fun1, L) == 1
    assert integrate(fun2, L) == 0
    assert integrate(-fun1, L) == -1
    assert integrate(-fun2, L) == 0
    assert integrate(fun_sum, L) == 1.
    assert integrate(-fun_sum, L) == -1.

