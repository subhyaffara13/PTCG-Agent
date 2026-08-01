
def test_issue_26495():
    nbar = Symbol('nbar', real=True, nonnegative=True)
    n = Symbol('n', integer=True)
    i = Symbol('i', integer=True, nonnegative=True)
    j = Symbol('j', integer=True, nonnegative=True)
    rho = Sum((nbar/(1+nbar))**n*SHOKet(n)*SHOBra(n), (n,0,oo))
    result = qapply(SHOBra(i)*rho*SHOKet(j), sum_doit=True)
    assert simplify(result) == (nbar/(nbar+1))**i*KroneckerDelta(i,j)

