
def test_singular():
    assert ask(Q.singular(X)) is None
    assert ask(Q.singular(X), Q.invertible(X)) is False
    assert ask(Q.singular(X), ~Q.invertible(X)) is True


def test_singular(problem_func):
    A, b = problem_func()
    A[0, ] = 0
    b[0] = 0
    xp, info = minres(A, b)
    assert_equal(info, 0)
    assert norm(A @ xp - b) <= 1e-5 * norm(b)


def test_singular():
    mp.dps = 15
    A = [[5.6, 1.2], [7./15, .1]]
    B = repr(zeros(2))
    b = [1, 2]
    for i in ['lu_solve(%s, %s)' % (A, b), 'lu_solve(%s, %s)' % (B, b),
              'qr_solve(%s, %s)' % (A, b), 'qr_solve(%s, %s)' % (B, b)]:
        pytest.raises((ZeroDivisionError, ValueError), lambda: eval(i))

