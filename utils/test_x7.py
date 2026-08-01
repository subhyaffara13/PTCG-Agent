
def test_X7():
    # => sum( Bernoulli[k]/k! x^(k - 2), k = 1..infinity )
    #    = 1/x^2 - 1/(2 x) + 1/12 - x^2/720 + x^4/30240 + O(x^6)
    #    [Levinson and Redheffer, p. 173]
    assert (series(1/(x*(exp(x) - 1)), x, 0, 7) == x**(-2) - 1/(2*x) +
            R(1, 12) - x**2/720 + x**4/30240 - x**6/1209600 + O(x**7))

