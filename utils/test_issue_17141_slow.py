
def test_issue_17141_slow():
    # Should not give RecursionError
    assert simplify((2**acos(I+1)**2).rewrite('log')) == 2**((pi + 2*I*log(-1 +
                   sqrt(1 - 2*I) + I))**2/4)

