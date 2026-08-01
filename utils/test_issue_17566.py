
def test_issue_17566():
    assert nonlinsolve([32*(2**x)/2**(-y) - 4**y, 27*(3**x) - S(1)/3**y], x, y) ==\
        FiniteSet((-log(81)/log(3), 1))

