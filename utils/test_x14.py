
def test_X14():
    # Wallis' product => 1/sqrt(pi n) + ...   [Knopp, p. 385]
    assert series(1/2**(2*n)*binomial(2*n, n),
                  n, x==oo, n=1) == 1/(sqrt(pi)*sqrt(n)) + O(1/x, (x, oo))

