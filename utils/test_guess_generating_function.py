
def test_guess_generating_function():
    x = Symbol('x')
    assert guess_generating_function([fibonacci(k)
        for k in range(5, 15)])['ogf'] == ((3*x + 5)/(-x**2 - x + 1))
    assert guess_generating_function(
        [1, 2, 5, 14, 41, 124, 383, 1200, 3799, 12122, 38919])['ogf'] == (
        (1/(x**4 + 2*x**2 - 4*x + 1))**S.Half)
    assert guess_generating_function(sympify(
       "[3/2, 11/2, 0, -121/2, -363/2, 121, 4719/2, 11495/2, -8712, -178717/2]")
       )['ogf'] == (x + Rational(3, 2))/(11*x**2 - 3*x + 1)
    assert guess_generating_function([factorial(k) for k in range(12)],
       types=['egf'])['egf'] == 1/(-x + 1)
    assert guess_generating_function([k+1 for k in range(12)],
       types=['egf']) == {'egf': (x + 1)*exp(x), 'lgdegf': (x + 2)/(x + 1)}

