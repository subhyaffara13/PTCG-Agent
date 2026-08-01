
def test_bernoulli_c_poly():
    raises(ValueError, lambda: bernoulli_c_poly(-1, x))
    assert bernoulli_c_poly(1, x, polys=True) == Poly(x, domain='QQ')

    assert bernoulli_c_poly(0, x) == 1
    assert bernoulli_c_poly(1, x) == x
    assert bernoulli_c_poly(2, x) == x**2 - Q(1,3)
    assert bernoulli_c_poly(3, x) == x**3 - x
    assert bernoulli_c_poly(4, x) == x**4 - 2*x**2 + Q(7,15)
    assert bernoulli_c_poly(5, x) == x**5 - Q(10,3)*x**3 + Q(7,3)*x
    assert bernoulli_c_poly(6, x) == x**6 - 5*x**4 + 7*x**2 - Q(31,21)

    assert bernoulli_c_poly(1).dummy_eq(x)
    assert bernoulli_c_poly(1, polys=True) == Poly(x, domain='QQ')

    assert 2**8 * bernoulli_poly(8, (x+1)/2).expand() == bernoulli_c_poly(8, x)
    assert 2**9 * bernoulli_poly(9, (x+1)/2).expand() == bernoulli_c_poly(9, x)

