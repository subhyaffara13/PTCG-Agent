
def test_constant_renumber():
    e1, e2, x, y = symbols("e1:3 x y")
    exprs = [e2*x, e1*x + e2*y]

    assert constant_renumber(exprs[0]) == e2*x
    assert constant_renumber(exprs[0], variables=[x]) == C1*x
    assert constant_renumber(exprs[0], variables=[x], newconstants=[C2]) == C2*x
    assert constant_renumber(exprs, variables=[x, y]) == [C1*x, C1*y + C2*x]
    assert constant_renumber(exprs, variables=[x, y], newconstants=symbols("C3:5")) == [C3*x, C3*y + C4*x]

