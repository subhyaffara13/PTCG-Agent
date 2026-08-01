
def test_issue_5910():
    t = Symbol('t')
    assert (1/(1 - t)).subs(t, 1) is zoo
    n = t
    d = t - 1
    assert (n/d).subs(t, 1) is zoo
    assert (-n/-d).subs(t, 1) is zoo

