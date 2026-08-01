
def test_AssocOp_doit():
    a = Add(x,x, evaluate=False)
    b = Mul(y,y, evaluate=False)
    c = Add(b,b, evaluate=False)
    d = Mul(a,a, evaluate=False)
    assert c.doit(deep=False).func == Mul
    assert c.doit(deep=False).args == (2,y,y)
    assert c.doit().func == Mul
    assert c.doit().args == (2, Pow(y,2))
    assert d.doit(deep=False).func == Pow
    assert d.doit(deep=False).args == (a, 2*S.One)
    assert d.doit().func == Mul
    assert d.doit().args == (4*S.One, Pow(x,2))

