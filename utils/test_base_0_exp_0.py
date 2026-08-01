
def test_base_0_exp_0():
    assert solve(0**x - 1) == [0]
    assert solve(0**(x - 2) - 1) == [2]
    assert solve(S('x*(1/x**0 - x)', evaluate=False)) == \
        [0, 1]

