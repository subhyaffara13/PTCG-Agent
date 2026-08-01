
def test_manualintegrate_sqrt_linear():
    assert_is_integral_of((5*x**3+4)/sqrt(2+3*x),
                          10*(3*x + 2)**(S(7)/2)/567 - 4*(3*x + 2)**(S(5)/2)/27 +
                          40*(3*x + 2)**(S(3)/2)/81 + 136*sqrt(3*x + 2)/81)
    assert manualintegrate(x/sqrt(a+b*x)**3, x) == \
        Piecewise((Mul(2, b**-2, a/sqrt(a + b*x) + sqrt(a + b*x)), Ne(b, 0)), (x**2/(2*a**(S(3)/2)), True))
    assert_is_integral_of((sqrt(3*x+3)+1)/((2*x+2)**(1/S(3))+1),
                          3*sqrt(6)*(2*x + 2)**(S(7)/6)/14 - 3*sqrt(6)*(2*x + 2)**(S(5)/6)/10 -
                          3*sqrt(6)*(2*x + 2)**(S.One/6)/2 + 3*(2*x + 2)**(S(2)/3)/4 - 3*(2*x + 2)**(S.One/3)/2 +
                          sqrt(6)*sqrt(2*x + 2)/2 + 3*log((2*x + 2)**(S.One/3) + 1)/2 +
                          3*sqrt(6)*atan((2*x + 2)**(S.One/6))/2)
    assert_is_integral_of(sqrt(x+sqrt(x)),
                          2*sqrt(sqrt(x) + x)*(sqrt(x)/12 + x/3 - S(1)/8) + log(2*sqrt(x) + 2*sqrt(sqrt(x) + x) + 1)/8)
    assert_is_integral_of(sqrt(2*x+3+sqrt(4*x+5))**3,
                          sqrt(2*x + sqrt(4*x + 5) + 3) *
                          (9*x/10 + 11*(4*x + 5)**(S(3)/2)/40 + sqrt(4*x + 5)/40 + (4*x + 5)**2/10 + S(11)/10)/2)

