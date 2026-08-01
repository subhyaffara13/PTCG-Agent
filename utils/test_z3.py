
def test_Z3():
    # => r(n) = Fibonacci[n + 1]   [Cohen, p. 83]
    r = Function('r')
    # recurrence solution is correct, Wester expects it to be simplified to
    # fibonacci(n+1), but that is quite hard
    expected = ((S(1)/2 - sqrt(5)/2)**n*(S(1)/2 - sqrt(5)/10)
              + (S(1)/2 + sqrt(5)/2)**n*(sqrt(5)/10 + S(1)/2))
    sol = rsolve(r(n) - (r(n - 1) + r(n - 2)), r(n), {r(1): 1, r(2): 2})
    assert sol == expected


def test_z3():
    z3 = import_module("z3")

    if not z3:
        skip("z3 not installed.")
    A, B, C = symbols('A,B,C')
    x, y, z = symbols('x,y,z')
    assert z3_satisfiable((x >= 2) & (x < 1)) is False
    assert z3_satisfiable( A & ~A ) is False

    model = z3_satisfiable(A & (~A | B | C))
    assert bool(model) is True
    assert model[A] is True

    # test nonlinear function
    assert z3_satisfiable((x ** 2 >= 2) & (x < 1) & (x > -1)) is False

