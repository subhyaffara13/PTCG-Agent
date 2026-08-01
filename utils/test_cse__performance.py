
def test_cse__performance():
    nexprs, nterms = 3, 20
    x = symbols('x:%d' % nterms)
    exprs = [
        reduce(add, [x[j]*(-1)**(i+j) for j in range(nterms)])
        for i in range(nexprs)
    ]
    assert (exprs[0] + exprs[1]).simplify() == 0
    subst, red = cse(exprs)
    assert len(subst) > 0, "exprs[0] == -exprs[2], i.e. a CSE"
    for i, e in enumerate(red):
        assert (e.subs(reversed(subst)) - exprs[i]).simplify() == 0

