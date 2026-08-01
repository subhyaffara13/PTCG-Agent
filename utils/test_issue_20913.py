
def test_issue_20913():
    assert Poly(x + 9671406556917067856609794, x).real_roots() == [-9671406556917067856609794]
    assert Poly(x**3 + 4, x).real_roots() == [-2**(S(2)/3)]

