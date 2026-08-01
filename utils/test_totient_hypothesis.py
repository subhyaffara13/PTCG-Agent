
def test_totient_hypothesis(n):
    assert totient(n) <= n
    div = divisors(n)
    totients = [totient(i) for i in div]
    assert n == sum(totients)

