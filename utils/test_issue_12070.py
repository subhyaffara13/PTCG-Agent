
def test_issue_12070():
    exprs = [x + y, 2 + x + y, x + y + z, 3 + x + y + z]
    subst, red = cse(exprs)
    assert 6 >= (len(subst) + sum(v.count_ops() for k, v in subst) +
                 count_ops(red))

