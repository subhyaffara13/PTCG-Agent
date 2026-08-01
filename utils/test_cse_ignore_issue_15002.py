
def test_cse_ignore_issue_15002():
    l = [
        w*exp(x)*exp(-z),
        exp(y)*exp(x)*exp(-z)
    ]
    substs, reduced = cse(l, ignore=(x,))
    rl = [e.subs(reversed(substs)) for e in reduced]
    assert rl == l

