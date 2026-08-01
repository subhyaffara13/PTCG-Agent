
def test_evalf_near_integers():
    # Binet's formula
    f = lambda n: ((1 + sqrt(5))**n)/(2**n * sqrt(5))
    assert NS(f(5000) - fibonacci(5000), 10, maxn=1500) == '5.156009964e-1046'
    # Some near-integer identities from
    # http://mathworld.wolfram.com/AlmostInteger.html
    assert NS('sin(2017*2**(1/5))', 15) == '-1.00000000000000'
    assert NS('sin(2017*2**(1/5))', 20) == '-0.99999999999999997857'
    assert NS('1+sin(2017*2**(1/5))', 15) == '2.14322287389390e-17'
    assert NS('45 - 613*E/37 + 35/991', 15) == '6.03764498766326e-11'

