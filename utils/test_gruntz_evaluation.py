
def test_gruntz_evaluation():
    # Gruntz' thesis pp. 122 to 123
    # 8.1
    assert gruntz(exp(x)*(exp(1/x - exp(-x)) - exp(1/x)), x, oo) == -1
    # 8.2
    assert gruntz(exp(x)*(exp(1/x + exp(-x) + exp(-x**2))
                  - exp(1/x - exp(-exp(x)))), x, oo) == 1
    # 8.3
    assert gruntz(exp(exp(x - exp(-x))/(1 - 1/x)) - exp(exp(x)), x, oo) is oo
    # 8.5
    assert gruntz(exp(exp(exp(x + exp(-x)))) / exp(exp(exp(x))), x, oo) is oo
    # 8.6
    assert gruntz(exp(exp(exp(x))) / exp(exp(exp(x - exp(-exp(x))))),
                  x, oo) is oo
    # 8.7
    assert gruntz(exp(exp(exp(x))) / exp(exp(exp(x - exp(-exp(exp(x)))))),
                  x, oo) == 1
    # 8.8
    assert gruntz(exp(exp(x)) / exp(exp(x - exp(-exp(exp(x))))), x, oo) == 1
    # 8.9
    assert gruntz(log(x)**2 * exp(sqrt(log(x))*(log(log(x)))**2
                  * exp(sqrt(log(log(x))) * (log(log(log(x))))**3)) / sqrt(x),
                  x, oo) == 0
    # 8.10
    assert gruntz((x*log(x)*(log(x*exp(x) - x**2))**2)
                  / (log(log(x**2 + 2*exp(exp(3*x**3*log(x)))))), x, oo) == Rational(1, 3)
    # 8.11
    assert gruntz((exp(x*exp(-x)/(exp(-x) + exp(-2*x**2/(x + 1)))) - exp(x))/x,
                  x, oo) == -exp(2)
    # 8.12
    assert gruntz((3**x + 5**x)**(1/x), x, oo) == 5
    # 8.13
    assert gruntz(x/log(x**(log(x**(log(2)/log(x))))), x, oo) is oo
    # 8.14
    assert gruntz(exp(exp(2*log(x**5 + x)*log(log(x))))
                  / exp(exp(10*log(x)*log(log(x)))), x, oo) is oo
    # 8.15
    assert gruntz(exp(exp(Rational(5, 2)*x**Rational(-5, 7) + Rational(21, 8)*x**Rational(6, 11)
                          + 2*x**(-8) + Rational(54, 17)*x**Rational(49, 45)))**8
                  / log(log(-log(Rational(4, 3)*x**Rational(-5, 14))))**Rational(7, 6), x, oo) is oo
    # 8.16
    assert gruntz((exp(4*x*exp(-x)/(1/exp(x) + 1/exp(2*x**2/(x + 1)))) - exp(x))
                  / exp(x)**4, x, oo) == 1
    # 8.17
    assert gruntz(exp(x*exp(-x)/(exp(-x) + exp(-2*x**2/(x + 1))))/exp(x), x, oo) \
        == 1
    # 8.19
    assert gruntz(log(x)*(log(log(x) + log(log(x))) - log(log(x)))
                  / (log(log(x) + log(log(log(x))))), x, oo) == 1
    # 8.20
    assert gruntz(exp((log(log(x + exp(log(x)*log(log(x))))))
                  / (log(log(log(exp(x) + x + log(x)))))), x, oo) == E
    # Another
    assert gruntz(exp(exp(exp(x + exp(-x)))) / exp(exp(x)), x, oo) is oo

