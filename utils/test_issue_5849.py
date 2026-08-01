
def test_issue_5849():
    #
    # XXX: This system does not have a solution for most values of the
    # parameters. Generally solve returns the empty set for systems that are
    # generically inconsistent.
    #
    I1, I2, I3, I4, I5, I6 = symbols('I1:7')
    dI1, dI4, dQ2, dQ4, Q2, Q4 = symbols('dI1,dI4,dQ2,dQ4,Q2,Q4')

    e = (
        I1 - I2 - I3,
        I3 - I4 - I5,
        I4 + I5 - I6,
        -I1 + I2 + I6,
        -2*I1 - 2*I3 - 2*I5 - 3*I6 - dI1/2 + 12,
        -I4 + dQ4,
        -I2 + dQ2,
        2*I3 + 2*I5 + 3*I6 - Q2,
        I4 - 2*I5 + 2*Q4 + dI4
    )

    ans = [{
    I1: I2 + I3,
    dI1: -4*I2 - 8*I3 - 4*I5 - 6*I6 + 24,
    I4: I3 - I5,
    dQ4: I3 - I5,
    Q4: -I3/2 + 3*I5/2 - dI4/2,
    dQ2: I2,
    Q2: 2*I3 + 2*I5 + 3*I6}]

    v = I1, I4, Q2, Q4, dI1, dI4, dQ2, dQ4
    assert solve(e, *v, manual=True, check=False, dict=True) == ans
    assert solve(e, *v, manual=True, check=False) == [
        tuple([a.get(i, i) for i in v]) for a in ans]
    assert solve(e, *v, manual=True) == []
    assert solve(e, *v) == []

    # the matrix solver (tested below) doesn't like this because it produces
    # a zero row in the matrix. Is this related to issue 4551?
    assert [ei.subs(
        ans[0]) for ei in e] == [0, 0, I3 - I6, -I3 + I6, 0, 0, 0, 0, 0]

