
def test_return_root_of():
    f = x**5 - 15*x**3 - 5*x**2 + 10*x + 20
    s = list(solveset_complex(f, x))
    for root in s:
        assert root.func == CRootOf

    # if one uses solve to get the roots of a polynomial that has a CRootOf
    # solution, make sure that the use of nfloat during the solve process
    # doesn't fail. Note: if you want numerical solutions to a polynomial
    # it is *much* faster to use nroots to get them than to solve the
    # equation only to get CRootOf solutions which are then numerically
    # evaluated. So for eq = x**5 + 3*x + 7 do Poly(eq).nroots() rather
    # than [i.n() for i in solve(eq)] to get the numerical roots of eq.
    assert nfloat(list(solveset_complex(x**5 + 3*x**3 + 7, x))[0],
                  exponent=False) == CRootOf(x**5 + 3*x**3 + 7, 0).n()

    sol = list(solveset_complex(x**6 - 2*x + 2, x))
    assert all(isinstance(i, CRootOf) for i in sol) and len(sol) == 6

    f = x**5 - 15*x**3 - 5*x**2 + 10*x + 20
    s = list(solveset_complex(f, x))
    for root in s:
        assert root.func == CRootOf

    s = x**5 + 4*x**3 + 3*x**2 + Rational(7, 4)
    assert solveset_complex(s, x) == \
        FiniteSet(*Poly(s*4, domain='ZZ').all_roots())

    # Refer issue #7876
    eq = x*(x - 1)**2*(x + 1)*(x**6 - x + 1)
    assert solveset_complex(eq, x) == \
        FiniteSet(-1, 0, 1, CRootOf(x**6 - x + 1, 0),
                       CRootOf(x**6 - x + 1, 1),
                       CRootOf(x**6 - x + 1, 2),
                       CRootOf(x**6 - x + 1, 3),
                       CRootOf(x**6 - x + 1, 4),
                       CRootOf(x**6 - x + 1, 5))

