
def test_solveset_complex_polynomial():
    assert solveset_complex(a*x**2 + b*x + c, x) == \
        FiniteSet(-b/(2*a) - sqrt(-4*a*c + b**2)/(2*a),
                  -b/(2*a) + sqrt(-4*a*c + b**2)/(2*a))

    assert solveset_complex(x - y**3, y) == FiniteSet(
        (-x**Rational(1, 3))/2 + I*sqrt(3)*x**Rational(1, 3)/2,
        x**Rational(1, 3),
        (-x**Rational(1, 3))/2 - I*sqrt(3)*x**Rational(1, 3)/2)

    assert solveset_complex(x + 1/x - 1, x) == \
        FiniteSet(S.Half + I*sqrt(3)/2, S.Half - I*sqrt(3)/2)

