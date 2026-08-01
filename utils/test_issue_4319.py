
def test_issue_4319():
    x, y = symbols('x y')

    p = -x*(S.One/8 - y)
    ans = {S.Zero, y - S.One/8}

    def ok(pat):
        assert set(p.match(pat).values()) == ans

    ok(Wild("coeff", exclude=[x])*x + Wild("rest"))
    ok(Wild("w", exclude=[x])*x + Wild("rest"))
    ok(Wild("coeff", exclude=[x])*x + Wild("rest"))
    ok(Wild("w", exclude=[x])*x + Wild("rest"))
    ok(Wild("e", exclude=[x])*x + Wild("rest"))
    ok(Wild("ress", exclude=[x])*x + Wild("rest"))
    ok(Wild("resu", exclude=[x])*x + Wild("rest"))

