
def test_issue_5849_matrix():
    '''Same as test_issue_5849 but solved with the matrix solver.

    A solution only exists if I3 == I6 which is not generically true,
    but `solve` does not return conditions under which the solution is
    valid, only a solution that is canonical and consistent with the input.
    '''
    # a simple example with the same issue
    # assert solve([x+y+z, x+y], [x, y]) == {x: y}
    # the longer example
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
    assert solve(e, I1, I4, Q2, Q4, dI1, dI4, dQ2, dQ4) == []

