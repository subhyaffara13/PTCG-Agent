
def test_issue_26903():
    p1 = nextprime(10**16)  # greater than 10**15
    p2 = nextprime(p1)
    assert sqrt(p1**2*p2).is_Pow  # square not extracted
    zero = sqrt(p1**2*p2) - p1*sqrt(p2)
    assert minimal_polynomial(zero, x) == x
    assert minimal_polynomial(sqrt(2) - zero, x) == x**2 - 2

