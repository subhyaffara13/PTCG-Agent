
def test_tribonacci():
    assert [tribonacci(n) for n in range(8)] == [0, 1, 1, 2, 4, 7, 13, 24]
    assert tribonacci(100) == 98079530178586034536500564

    assert tribonacci(0, x) == 0
    assert tribonacci(1, x) == 1
    assert tribonacci(2, x) == x**2
    assert tribonacci(3, x) == x**4 + x
    assert tribonacci(4, x) == x**6 + 2*x**3 + 1
    assert tribonacci(5, x) == x**8 + 3*x**5 + 3*x**2

    n = Dummy('n')
    assert tribonacci(n).limit(n, S.Infinity) is S.Infinity

    w = (-1 + S.ImaginaryUnit * sqrt(3)) / 2
    a = (1 + cbrt(19 + 3*sqrt(33)) + cbrt(19 - 3*sqrt(33))) / 3
    b = (1 + w*cbrt(19 + 3*sqrt(33)) + w**2*cbrt(19 - 3*sqrt(33))) / 3
    c = (1 + w**2*cbrt(19 + 3*sqrt(33)) + w*cbrt(19 - 3*sqrt(33))) / 3
    assert tribonacci(n).rewrite(sqrt) == \
      (a**(n + 1)/((a - b)*(a - c))
      + b**(n + 1)/((b - a)*(b - c))
      + c**(n + 1)/((c - a)*(c - b)))
    assert tribonacci(n).rewrite(sqrt).subs(n, 4).simplify() == tribonacci(4)
    assert tribonacci(n).rewrite(GoldenRatio).subs(n,10).evalf() == \
        Float(tribonacci(10))
    assert tribonacci(n).rewrite(TribonacciConstant) == floor(
            3*TribonacciConstant**n*(102*sqrt(33) + 586)**Rational(1, 3)/
            (-2*(102*sqrt(33) + 586)**Rational(1, 3) + 4 + (102*sqrt(33)
            + 586)**Rational(2, 3)) + S.Half)
    raises(ValueError, lambda: tribonacci(-1, x))

