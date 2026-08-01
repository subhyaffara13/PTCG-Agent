
def test_issue_6350():
    expr = integrate(exp(k*(y**3 - 3*y)), (y, 0, oo), conds='none')
    assert expr.series(k, 0, 3) == -(-1)**(S(2)/3)*sqrt(3)*gamma(S(1)/3)**2*gamma(S(2)/3)/(6*pi*k**(S(1)/3)) - \
        sqrt(3)*k*gamma(-S(2)/3)*gamma(-S(1)/3)/(6*pi) - \
        (-1)**(S(1)/3)*sqrt(3)*k**(S(1)/3)*gamma(-S(1)/3)*gamma(S(1)/3)*gamma(S(2)/3)/(6*pi) - \
        (-1)**(S(2)/3)*sqrt(3)*k**(S(5)/3)*gamma(S(1)/3)**2*gamma(S(2)/3)/(4*pi) - \
        (-1)**(S(1)/3)*sqrt(3)*k**(S(7)/3)*gamma(-S(1)/3)*gamma(S(1)/3)*gamma(S(2)/3)/(8*pi) + O(k**3)

