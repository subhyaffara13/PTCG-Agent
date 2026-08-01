
def test_trigsimp_old():
    x, y = symbols('x,y')

    assert trigsimp(1 - sin(x)**2, old=True) == cos(x)**2
    assert trigsimp(1 - cos(x)**2, old=True) == sin(x)**2
    assert trigsimp(sin(x)**2 + cos(x)**2, old=True) == 1
    assert trigsimp(1 + tan(x)**2, old=True) == 1/cos(x)**2
    assert trigsimp(1/cos(x)**2 - 1, old=True) == tan(x)**2
    assert trigsimp(1/cos(x)**2 - tan(x)**2, old=True) == 1
    assert trigsimp(1 + cot(x)**2, old=True) == 1/sin(x)**2
    assert trigsimp(1/sin(x)**2 - cot(x)**2, old=True) == 1

    assert trigsimp(5*cos(x)**2 + 5*sin(x)**2, old=True) == 5

    assert trigsimp(sin(x)/cos(x), old=True) == tan(x)
    assert trigsimp(2*tan(x)*cos(x), old=True) == 2*sin(x)
    assert trigsimp(cot(x)**3*sin(x)**3, old=True) == cos(x)**3
    assert trigsimp(y*tan(x)**2/sin(x)**2, old=True) == y/cos(x)**2
    assert trigsimp(cot(x)/cos(x), old=True) == 1/sin(x)

    assert trigsimp(sin(x + y) + sin(x - y), old=True) == 2*sin(x)*cos(y)
    assert trigsimp(sin(x + y) - sin(x - y), old=True) == 2*sin(y)*cos(x)
    assert trigsimp(cos(x + y) + cos(x - y), old=True) == 2*cos(x)*cos(y)
    assert trigsimp(cos(x + y) - cos(x - y), old=True) == -2*sin(x)*sin(y)

    assert trigsimp(sinh(x + y) + sinh(x - y), old=True) == 2*sinh(x)*cosh(y)
    assert trigsimp(sinh(x + y) - sinh(x - y), old=True) == 2*sinh(y)*cosh(x)
    assert trigsimp(cosh(x + y) + cosh(x - y), old=True) == 2*cosh(x)*cosh(y)
    assert trigsimp(cosh(x + y) - cosh(x - y), old=True) == 2*sinh(x)*sinh(y)

    assert trigsimp(cos(0.12345)**2 + sin(0.12345)**2, old=True) == 1.0

    assert trigsimp(sin(x)/cos(x), old=True, method='combined') == tan(x)
    assert trigsimp(sin(x)/cos(x), old=True, method='groebner') == sin(x)/cos(x)
    assert trigsimp(sin(x)/cos(x), old=True, method='groebner', hints=[tan]) == tan(x)

    assert trigsimp(1-sin(sin(x)**2+cos(x)**2)**2, old=True, deep=True) == cos(1)**2

