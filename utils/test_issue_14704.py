
def test_issue_14704():
    a = 144**144
    x, xexact = integer_nthroot(a,a)
    assert x == 1 and xexact is False

