
def test_issue_13947():
    a, t, s = symbols('a t s')
    assert risch_integrate(2**(-pi)/(2**t + 1), t) == \
        2**(-pi)*t - 2**(-pi)*log(2**t + 1)/log(2)
    assert risch_integrate(a**(t - s)/(a**t + 1), t) == \
        exp(-s*log(a))*log(a**t + 1)/log(a)

