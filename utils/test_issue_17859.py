
def test_issue_17859():
    r = Range(-oo,oo)
    raises(ValueError,lambda: r[::2])
    raises(ValueError, lambda: r[::-2])
    r = Range(oo,-oo,-1)
    raises(ValueError,lambda: r[::2])
    raises(ValueError, lambda: r[::-2])

