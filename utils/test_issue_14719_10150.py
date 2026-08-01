
def test_issue_14719_10150():
    class V(Expr):
        _diff_wrt = True
        is_scalar = False
    assert V().diff(V()) == Derivative(V(), V())
    assert (2*V()).diff(V()) == 2*Derivative(V(), V())
    class X(Expr):
        _diff_wrt = True
    assert X().diff(X()) == 1
    assert (2*X()).diff(X()) == 2

