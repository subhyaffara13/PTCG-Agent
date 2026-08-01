
def test_posify():
    x = symbols('x')

    assert str(posify(
        x +
        Symbol('p', positive=True) +
        Symbol('n', negative=True))) == '(_x + n + p, {_x: x})'

    eq, rep = posify(1/x)
    assert log(eq).expand().subs(rep) == -log(x)
    assert str(posify([x, 1 + x])) == '([_x, _x + 1], {_x: x})'

    p = symbols('p', positive=True)
    n = symbols('n', negative=True)
    orig = [x, n, p]
    modified, reps = posify(orig)
    assert str(modified) == '[_x, n, p]'
    assert [w.subs(reps) for w in modified] == orig

    assert str(Integral(posify(1/x + y)[0], (y, 1, 3)).expand()) == \
        'Integral(1/_x, (y, 1, 3)) + Integral(_y, (y, 1, 3))'
    assert str(Sum(posify(1/x**n)[0], (n,1,3)).expand()) == \
        'Sum(_x**(-n), (n, 1, 3))'

    A = Matrix([[1, 2, 3], [4, 5, 6 * Abs(x)]])
    Ap, rep = posify(A)
    assert Ap == A.subs(*reversed(rep.popitem()))

    # issue 16438
    k = Symbol('k', finite=True)
    eq, rep = posify(k)
    assert eq.assumptions0 == {'positive': True, 'zero': False, 'imaginary': False,
     'nonpositive': False, 'commutative': True, 'hermitian': True, 'real': True, 'nonzero': True,
     'nonnegative': True, 'negative': False, 'complex': True, 'finite': True,
     'infinite': False, 'extended_real':True, 'extended_negative': False,
     'extended_nonnegative': True, 'extended_nonpositive': False,
     'extended_nonzero': True, 'extended_positive': True}


def test_posify():
    assert posify(A)[0].is_commutative is False
    for q in (A*B/A, (A*B/A)**2, (A*B)**2, A*B - B*A):
        p = posify(q)
        assert p[0].subs(p[1]) == q

