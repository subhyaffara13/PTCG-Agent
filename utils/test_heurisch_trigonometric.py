
def test_heurisch_trigonometric():
    assert heurisch(sin(x), x) == -cos(x)
    assert heurisch(pi*sin(x) + 1, x) == x - pi*cos(x)

    assert heurisch(cos(x), x) == sin(x)
    assert heurisch(tan(x), x) in [
        log(1 + tan(x)**2)/2,
        log(tan(x) + I) + I*x,
        log(tan(x) - I) - I*x,
    ]

    assert heurisch(sin(x)*sin(y), x) == -cos(x)*sin(y)
    assert heurisch(sin(x)*sin(y), y) == -cos(y)*sin(x)

    # gives sin(x) in answer when run via setup.py and cos(x) when run via py.test
    assert heurisch(sin(x)*cos(x), x) in [sin(x)**2 / 2, -cos(x)**2 / 2]
    assert heurisch(cos(x)/sin(x), x) == log(sin(x))

    assert heurisch(x*sin(7*x), x) == sin(7*x) / 49 - x*cos(7*x) / 7
    assert heurisch(1/pi/4 * x**2*cos(x), x) == 1/pi/4*(x**2*sin(x) -
                    2*sin(x) + 2*x*cos(x))

    assert heurisch(acos(x/4) * asin(x/4), x) == 2*x - (sqrt(16 - x**2))*asin(x/4) \
        + (sqrt(16 - x**2))*acos(x/4) + x*asin(x/4)*acos(x/4)

    assert heurisch(sin(x)/(cos(x)**2+1), x) == -atan(cos(x)) #fixes issue 13723
    assert heurisch(1/(cos(x)+2), x) == 2*sqrt(3)*atan(sqrt(3)*tan(x/2)/3)/3
    assert heurisch(2*sin(x)*cos(x)/(sin(x)**4 + 1), x) == atan(sqrt(2)*sin(x)
        - 1) - atan(sqrt(2)*sin(x) + 1)

    assert heurisch(1/cosh(x), x) == 2*atan(tanh(x/2))

