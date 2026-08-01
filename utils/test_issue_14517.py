
def test_issue_14517():
    M = Matrix([
        [   0, 10*I,    10*I,       0],
        [10*I,    0,       0,    10*I],
        [10*I,    0, 5 + 2*I,    10*I],
        [   0, 10*I,    10*I, 5 + 2*I]])
    ev = M.eigenvals()
    # test one random eigenvalue, the computation is a little slow
    test_ev = random.choice(list(ev.keys()))
    assert (M - test_ev*eye(4)).det() == 0

