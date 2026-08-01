
def test_tau_hypothesis(n):
    div = divisors(n)
    tau_n = len(div)
    assert is_square(n) == (tau_n % 2 == 1)
    sigmas = [divisor_sigma(i) for i in div]
    totients = [totient(n // i) for i in div]
    mul = [a * b for a, b in zip(sigmas, totients)]
    assert n * tau_n == sum(mul)

