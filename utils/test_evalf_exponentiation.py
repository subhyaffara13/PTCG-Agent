
def test_evalf_exponentiation():
    assert NS(sqrt(-pi)) == '1.77245385090552*I'
    assert NS(Pow(pi*I, Rational(
        1, 2), evaluate=False)) == '1.25331413731550 + 1.25331413731550*I'
    assert NS(pi**I) == '0.413292116101594 + 0.910598499212615*I'
    assert NS(pi**(E + I/3)) == '20.8438653991931 + 8.36343473930031*I'
    assert NS((pi + I/3)**(E + I/3)) == '17.2442906093590 + 13.6839376767037*I'
    assert NS(exp(pi)) == '23.1406926327793'
    assert NS(exp(pi + E*I)) == '-21.0981542849657 + 9.50576358282422*I'
    assert NS(pi**pi) == '36.4621596072079'
    assert NS((-pi)**pi) == '-32.9138577418939 - 15.6897116534332*I'
    assert NS((-pi)**(-pi)) == '-0.0247567717232697 + 0.0118013091280262*I'

