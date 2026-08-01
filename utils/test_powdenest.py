
def test_powdenest():
    x, y = symbols('x,y')
    p, q = symbols('p q', positive=True)
    i, j = symbols('i,j', integer=True)

    assert powdenest(x) == x
    assert powdenest(x + 2*(x**(a*Rational(2, 3)))**(3*x)) == (x + 2*(x**(a*Rational(2, 3)))**(3*x))
    assert powdenest((exp(a*Rational(2, 3)))**(3*x))  # -X-> (exp(a/3))**(6*x)
    assert powdenest((x**(a*Rational(2, 3)))**(3*x)) == ((x**(a*Rational(2, 3)))**(3*x))
    assert powdenest(exp(3*x*log(2))) == 2**(3*x)
    assert powdenest(sqrt(p**2)) == p
    eq = p**(2*i)*q**(4*i)
    assert powdenest(eq) == (p*q**2)**(2*i)
    # -X-> (x**x)**i*(x**x)**j == x**(x*(i + j))
    assert powdenest((x**x)**(i + j))
    assert powdenest(exp(3*y*log(x))) == x**(3*y)
    assert powdenest(exp(y*(log(a) + log(b)))) == (a*b)**y
    assert powdenest(exp(3*(log(a) + log(b)))) == a**3*b**3
    assert powdenest(((x**(2*i))**(3*y))**x) == ((x**(2*i))**(3*y))**x
    assert powdenest(((x**(2*i))**(3*y))**x, force=True) == x**(6*i*x*y)
    assert powdenest(((x**(a*Rational(2, 3)))**(3*y/i))**x) == \
        (((x**(a*Rational(2, 3)))**(3*y/i))**x)
    assert powdenest((x**(2*i)*y**(4*i))**z, force=True) == (x*y**2)**(2*i*z)
    assert powdenest((p**(2*i)*q**(4*i))**j) == (p*q**2)**(2*i*j)
    e = ((p**(2*a))**(3*y))**x
    assert powdenest(e) == e
    e = ((x**2*y**4)**a)**(x*y)
    assert powdenest(e) == e
    e = (((x**2*y**4)**a)**(x*y))**3
    assert powdenest(e) == ((x**2*y**4)**a)**(3*x*y)
    assert powdenest((((x**2*y**4)**a)**(x*y)), force=True) == \
        (x*y**2)**(2*a*x*y)
    assert powdenest((((x**2*y**4)**a)**(x*y))**3, force=True) == \
        (x*y**2)**(6*a*x*y)
    assert powdenest((x**2*y**6)**i) != (x*y**3)**(2*i)
    x, y = symbols('x,y', positive=True)
    assert powdenest((x**2*y**6)**i) == (x*y**3)**(2*i)

    assert powdenest((x**(i*Rational(2, 3))*y**(i/2))**(2*i)) == (x**Rational(4, 3)*y)**(i**2)
    assert powdenest(sqrt(x**(2*i)*y**(6*i))) == (x*y**3)**i

    assert powdenest(4**x) == 2**(2*x)
    assert powdenest((4**x)**y) == 2**(2*x*y)
    assert powdenest(4**x*y) == 2**(2*x)*y

