
def test_issue_10169():
    eq = S(-8*a - x**5*(a + b + c + e) - x**4*(4*a - 2**Rational(3,4)*c + 4*c +
        d + 2**Rational(3,4)*e + 4*e + k) - x**3*(-4*2**Rational(3,4)*c + sqrt(2)*c -
        2**Rational(3,4)*d + 4*d + sqrt(2)*e + 4*2**Rational(3,4)*e + 2**Rational(3,4)*k + 4*k) -
        x**2*(4*sqrt(2)*c - 4*2**Rational(3,4)*d + sqrt(2)*d + 4*sqrt(2)*e +
        sqrt(2)*k + 4*2**Rational(3,4)*k) - x*(2*a + 2*b + 4*sqrt(2)*d +
        4*sqrt(2)*k) + 5)
    assert solve_undetermined_coeffs(eq, [a, b, c, d, e, k], x) == {
        a: Rational(5,8),
        b: Rational(-5,1032),
        c: Rational(-40,129) - 5*2**Rational(3,4)/129 + 5*2**Rational(1,4)/1032,
        d: -20*2**Rational(3,4)/129 - 10*sqrt(2)/129 - 5*2**Rational(1,4)/258,
        e: Rational(-40,129) - 5*2**Rational(1,4)/1032 + 5*2**Rational(3,4)/129,
        k: -10*sqrt(2)/129 + 5*2**Rational(1,4)/258 + 20*2**Rational(3,4)/129
    }

