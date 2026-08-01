
def test_trigsimp_noncommutative():
    x, y = symbols('x,y')
    A, B = symbols('A,B', commutative=False)

    assert trigsimp(A - A*sin(x)**2) == A*cos(x)**2
    assert trigsimp(A - A*cos(x)**2) == A*sin(x)**2
    assert trigsimp(A*sin(x)**2 + A*cos(x)**2) == A
    assert trigsimp(A + A*tan(x)**2) == A/cos(x)**2
    assert trigsimp(A/cos(x)**2 - A) == A*tan(x)**2
    assert trigsimp(A/cos(x)**2 - A*tan(x)**2) == A
    assert trigsimp(A + A*cot(x)**2) == A/sin(x)**2
    assert trigsimp(A/sin(x)**2 - A) == A/tan(x)**2
    assert trigsimp(A/sin(x)**2 - A*cot(x)**2) == A

    assert trigsimp(y*A*cos(x)**2 + y*A*sin(x)**2) == y*A

    assert trigsimp(A*sin(x)/cos(x)) == A*tan(x)
    assert trigsimp(A*tan(x)*cos(x)) == A*sin(x)
    assert trigsimp(A*cot(x)**3*sin(x)**3) == A*cos(x)**3
    assert trigsimp(y*A*tan(x)**2/sin(x)**2) == y*A/cos(x)**2
    assert trigsimp(A*cot(x)/cos(x)) == A/sin(x)

    assert trigsimp(A*sin(x + y) + A*sin(x - y)) == 2*A*sin(x)*cos(y)
    assert trigsimp(A*sin(x + y) - A*sin(x - y)) == 2*A*sin(y)*cos(x)
    assert trigsimp(A*cos(x + y) + A*cos(x - y)) == 2*A*cos(x)*cos(y)
    assert trigsimp(A*cos(x + y) - A*cos(x - y)) == -2*A*sin(x)*sin(y)

    assert trigsimp(A*sinh(x + y) + A*sinh(x - y)) == 2*A*sinh(x)*cosh(y)
    assert trigsimp(A*sinh(x + y) - A*sinh(x - y)) == 2*A*sinh(y)*cosh(x)
    assert trigsimp(A*cosh(x + y) + A*cosh(x - y)) == 2*A*cosh(x)*cosh(y)
    assert trigsimp(A*cosh(x + y) - A*cosh(x - y)) == 2*A*sinh(x)*sinh(y)

    assert trigsimp(A*cos(0.12345)**2 + A*sin(0.12345)**2) == 1.0*A

