
def test_sqrt_quadratic():
    assert integrate(1/sqrt(3*x**2+4*x+5)) == sqrt(3)*asinh(3*sqrt(11)*(x + S(2)/3)/11)/3
    assert integrate(1/sqrt(-3*x**2+4*x+5)) == sqrt(3)*asin(3*sqrt(19)*(x - S(2)/3)/19)/3
    assert integrate(1/sqrt(3*x**2+4*x-5)) == sqrt(3)*log(6*x + 2*sqrt(3)*sqrt(3*x**2 + 4*x - 5) + 4)/3
    assert integrate(1/sqrt(4*x**2-4*x+1)) == (x - S.Half)*log(x - S.Half)/(2*sqrt((x - S.Half)**2))
    assert integrate(1/sqrt(a+b*x+c*x**2), x) == \
        Piecewise((log(b + 2*sqrt(c)*sqrt(a + b*x + c*x**2) + 2*c*x)/sqrt(c), Ne(c, 0) & Ne(a - b**2/(4*c), 0)),
                  ((b/(2*c) + x)*log(b/(2*c) + x)/sqrt(c*(b/(2*c) + x)**2), Ne(c, 0)),
                  (2*sqrt(a + b*x)/b, Ne(b, 0)), (x/sqrt(a), True))

    assert integrate((7*x+6)/sqrt(3*x**2+4*x+5)) == \
           7*sqrt(3*x**2 + 4*x + 5)/3 + 4*sqrt(3)*asinh(3*sqrt(11)*(x + S(2)/3)/11)/9
    assert integrate((7*x+6)/sqrt(-3*x**2+4*x+5)) == \
           -7*sqrt(-3*x**2 + 4*x + 5)/3 + 32*sqrt(3)*asin(3*sqrt(19)*(x - S(2)/3)/19)/9
    assert integrate((7*x+6)/sqrt(3*x**2+4*x-5)) == \
           7*sqrt(3*x**2 + 4*x - 5)/3 + 4*sqrt(3)*log(6*x + 2*sqrt(3)*sqrt(3*x**2 + 4*x - 5) + 4)/9
    assert integrate((d+e*x)/sqrt(a+b*x+c*x**2), x) == \
        Piecewise(((-b*e/(2*c) + d) *
                   Piecewise((log(b + 2*sqrt(c)*sqrt(a + b*x + c*x**2) + 2*c*x)/sqrt(c), Ne(a - b**2/(4*c), 0)),
                             ((b/(2*c) + x)*log(b/(2*c) + x)/sqrt(c*(b/(2*c) + x)**2), True)) +
                   e*sqrt(a + b*x + c*x**2)/c, Ne(c, 0)),
                  ((2*d*sqrt(a + b*x) + 2*e*(-a*sqrt(a + b*x) + (a + b*x)**(S(3)/2)/3)/b)/b, Ne(b, 0)),
                  ((d*x + e*x**2/2)/sqrt(a), True))

    assert integrate((3*x**3-x**2+2*x-4)/sqrt(x**2-3*x+2)) == \
           sqrt(x**2 - 3*x + 2)*(x**2 + 13*x/4 + S(101)/8) + 135*log(2*x + 2*sqrt(x**2 - 3*x + 2) - 3)/16

    assert integrate(sqrt(53225*x**2-66732*x+23013)) == \
           (x/2 - S(16683)/53225)*sqrt(53225*x**2 - 66732*x + 23013) + \
           111576969*sqrt(2129)*asinh(53225*x/10563 - S(11122)/3521)/1133160250
    assert integrate(sqrt(a+b*x+c*x**2), x) == \
        Piecewise(((a/2 - b**2/(8*c)) *
                   Piecewise((log(b + 2*sqrt(c)*sqrt(a + b*x + c*x**2) + 2*c*x)/sqrt(c), Ne(a - b**2/(4*c), 0)),
                             ((b/(2*c) + x)*log(b/(2*c) + x)/sqrt(c*(b/(2*c) + x)**2), True)) +
                   (b/(4*c) + x/2)*sqrt(a + b*x + c*x**2), Ne(c, 0)),
                  (2*(a + b*x)**(S(3)/2)/(3*b), Ne(b, 0)),
                  (sqrt(a)*x, True))

    assert integrate(x*sqrt(x**2+2*x+4)) == \
        (x**2/3 + x/6 + S(5)/6)*sqrt(x**2 + 2*x + 4) - 3*asinh(sqrt(3)*(x + 1)/3)/2

