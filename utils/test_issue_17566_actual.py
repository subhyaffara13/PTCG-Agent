
def test_issue_17566_actual():
    sys = [2**x + 2**y - 3, 4**x + 9**y - 5]
    # Not clear this is the correct result, but at least no recursion error
    assert nonlinsolve(sys, x, y) == FiniteSet((log(3 - 2**y)/log(2), y))

