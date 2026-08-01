
def test_issue_20733():
    expr = 1/((x - 9)*(x - 8)*(x - 7)*(x - 4)**2*(x - 3)**3*(x - 2))
    assert str(expr.evalf(1, subs={x:1})) == '-4.e-5'
    assert str(expr.evalf(2, subs={x:1})) == '-4.1e-5'
    assert str(expr.evalf(11, subs={x:1})) == '-4.1335978836e-5'
    assert str(expr.evalf(20, subs={x:1})) == '-0.000041335978835978835979'

    expr = Mul(*((x - i) for i in range(2, 1000)))
    assert srepr(expr.evalf(2, subs={x: 1})) == "Float('4.0271e+2561', precision=10)"
    assert srepr(expr.evalf(10, subs={x: 1})) == "Float('4.02790050126e+2561', precision=37)"
    assert srepr(expr.evalf(53, subs={x: 1})) == "Float('4.0279005012722099453824067459760158730668154575647110393e+2561', precision=179)"

