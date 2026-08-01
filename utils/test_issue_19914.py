
def test_issue_19914():
    a = Integer(-8)
    b = Integer(-1)
    r = Integer(63)
    d2 = a*a - b*b*r

    assert _sqrt_numeric_denest(a, b, r, d2) == \
        sqrt(14)*I/2 + 3*sqrt(2)*I/2
    assert sqrtdenest(sqrt(-8-sqrt(63))) == sqrt(14)*I/2 + 3*sqrt(2)*I/2

