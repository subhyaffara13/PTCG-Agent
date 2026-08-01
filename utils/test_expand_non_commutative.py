
def test_expand_non_commutative():
    A = Symbol('A', commutative=False)
    B = Symbol('B', commutative=False)
    C = Symbol('C', commutative=False)
    a = Symbol('a')
    b = Symbol('b')
    i = Symbol('i', integer=True)
    n = Symbol('n', negative=True)
    m = Symbol('m', negative=True)
    p = Symbol('p', polar=True)
    np = Symbol('p', polar=False)

    assert (C*(A + B)).expand() == C*A + C*B
    assert (C*(A + B)).expand() != A*C + B*C
    assert ((A + B)**2).expand() == A**2 + A*B + B*A + B**2
    assert ((A + B)**3).expand() == (A**2*B + B**2*A + A*B**2 + B*A**2 +
                                     A**3 + B**3 + A*B*A + B*A*B)
    # issue 6219
    assert ((a*A*B*A**-1)**2).expand() == a**2*A*B**2/A
    # Note that (a*A*B*A**-1)**2 is automatically converted to a**2*(A*B*A**-1)**2
    assert ((a*A*B*A**-1)**2).expand(deep=False) == a**2*(A*B*A**-1)**2
    assert ((a*A*B*A**-1)**2).expand() == a**2*(A*B**2*A**-1)
    assert ((a*A*B*A**-1)**2).expand(force=True) == a**2*A*B**2*A**(-1)
    assert ((a*A*B)**2).expand() == a**2*A*B*A*B
    assert ((a*A)**2).expand() == a**2*A**2
    assert ((a*A*B)**i).expand() == a**i*(A*B)**i
    assert ((a*A*(B*(A*B/A)**2))**i).expand() == a**i*(A*B*A*B**2/A)**i
    # issue 6558
    assert (A*B*(A*B)**-1).expand() == 1
    assert ((a*A)**i).expand() == a**i*A**i
    assert ((a*A*B*A**-1)**3).expand() == a**3*A*B**3/A
    assert ((a*A*B*A*B/A)**3).expand() == \
        a**3*A*B*(A*B**2)*(A*B**2)*A*B*A**(-1)
    assert ((a*A*B*A*B/A)**-2).expand() == \
        A*B**-1*A**-1*B**-2*A**-1*B**-1*A**-1/a**2
    assert ((a*b*A*B*A**-1)**i).expand() == a**i*b**i*(A*B/A)**i
    assert ((a*(a*b)**i)**i).expand() == a**i*a**(i**2)*b**(i**2)
    e = Pow(Mul(a, 1/a, A, B, evaluate=False), S(2), evaluate=False)
    assert e.expand() == A*B*A*B
    assert sqrt(a*(A*b)**i).expand() == sqrt(a*b**i*A**i)
    assert (sqrt(-a)**a).expand() == sqrt(-a)**a
    assert expand((-2*n)**(i/3)) == 2**(i/3)*(-n)**(i/3)
    assert expand((-2*n*m)**(i/a)) == (-2)**(i/a)*(-n)**(i/a)*(-m)**(i/a)
    assert expand((-2*a*p)**b) == 2**b*p**b*(-a)**b
    assert expand((-2*a*np)**b) == 2**b*(-a*np)**b
    assert expand(sqrt(A*B)) == sqrt(A*B)
    assert expand(sqrt(-2*a*b)) == sqrt(2)*sqrt(-a*b)

