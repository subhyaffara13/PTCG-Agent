
def test_evalf_integer_parts():
    a = floor(log(8)/log(2) - exp(-1000), evaluate=False)
    b = floor(log(8)/log(2), evaluate=False)
    assert a.evalf() == 3.0
    assert b.evalf() == 3.0
    # equals, as a fallback, can still fail but it might succeed as here
    assert ceiling(10*(sin(1)**2 + cos(1)**2)) == 10

    assert int(floor(factorial(50)/E, evaluate=False).evalf(70)) == \
        int(11188719610782480504630258070757734324011354208865721592720336800)
    assert int(ceiling(factorial(50)/E, evaluate=False).evalf(70)) == \
        int(11188719610782480504630258070757734324011354208865721592720336801)
    assert int(floor(GoldenRatio**999 / sqrt(5) + S.Half)
               .evalf(1000)) == fibonacci(999)
    assert int(floor(GoldenRatio**1000 / sqrt(5) + S.Half)
               .evalf(1000)) == fibonacci(1000)

    assert ceiling(x).evalf(subs={x: 3}) == 3.0
    assert ceiling(x).evalf(subs={x: 3*I}) == 3.0*I
    assert ceiling(x).evalf(subs={x: 2 + 3*I}) == 2.0 + 3.0*I
    assert ceiling(x).evalf(subs={x: 3.}) == 3.0
    assert ceiling(x).evalf(subs={x: 3.*I}) == 3.0*I
    assert ceiling(x).evalf(subs={x: 2. + 3*I}) == 2.0 + 3.0*I

    assert float((floor(1.5, evaluate=False)+1/9).evalf()) == 1 + 1/9
    assert float((floor(0.5, evaluate=False)+20).evalf()) == 20

    # issue 19991
    n = 1169809367327212570704813632106852886389036911
    r = 744723773141314414542111064094745678855643068

    assert floor(n / (pi / 2)) == r
    assert floor(80782 * sqrt(2)) == 114242

    # issue 20076
    assert 260515 - floor(260515/pi + 1/2) * pi == atan(tan(260515))

    assert floor(x).evalf(subs={x: sqrt(2)}) == 1.0

