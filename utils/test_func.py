
def test_func():
    e = 4.0*sympy.exp(-a)
    f = g.llvm_callable([a], e)
    res = float(e.subs({a: 1.5}).evalf())
    jit_res = f(1.5)

    assert isclose(jit_res, res)


def test_func():
    from sympy.simplify.simplify import nthroot

    A = Matrix([[1, 2],[0, 3]])
    assert A.analytic_func(sin(x*t), x) == Matrix([[sin(t), sin(3*t) - sin(t)], [0, sin(3*t)]])

    A = Matrix([[2, 1],[1, 2]])
    assert (pi * A / 6).analytic_func(cos(x), x) == Matrix([[sqrt(3)/4, -sqrt(3)/4], [-sqrt(3)/4, sqrt(3)/4]])


    raises(ValueError, lambda : zeros(5).analytic_func(log(x), x))
    raises(ValueError, lambda : (A*x).analytic_func(log(x), x))

    A = Matrix([[0, -1, -2, 3], [0, -1, -2, 3], [0, 1, 0, -1], [0, 0, -1, 1]])
    assert A.analytic_func(exp(x), x) == A.exp()
    raises(ValueError, lambda : A.analytic_func(sqrt(x), x))

    A = Matrix([[41, 12],[12, 34]])
    assert simplify(A.analytic_func(sqrt(x), x)**2) == A

    A = Matrix([[3, -12, 4], [-1, 0, -2], [-1, 5, -1]])
    assert simplify(A.analytic_func(nthroot(x, 3), x)**3) == A

    A = Matrix([[2, 0, 0, 0], [1, 2, 0, 0], [0, 1, 3, 0], [0, 0, 1, 3]])
    assert A.analytic_func(exp(x), x) == A.exp()

    A = Matrix([[0, 2, 1, 6], [0, 0, 1, 2], [0, 0, 0, 3], [0, 0, 0, 0]])
    assert A.analytic_func(exp(x*t), x) == expand(simplify((A*t).exp()))


def test_func():
    from sympy.simplify.simplify import nthroot

    A = Matrix([[1, 2],[0, 3]])
    assert A.analytic_func(sin(x*t), x) == Matrix([[sin(t), sin(3*t) - sin(t)], [0, sin(3*t)]])

    A = Matrix([[2, 1],[1, 2]])
    assert (pi * A / 6).analytic_func(cos(x), x) == Matrix([[sqrt(3)/4, -sqrt(3)/4], [-sqrt(3)/4, sqrt(3)/4]])


    raises(ValueError, lambda : zeros(5).analytic_func(log(x), x))
    raises(ValueError, lambda : (A*x).analytic_func(log(x), x))

    A = Matrix([[0, -1, -2, 3], [0, -1, -2, 3], [0, 1, 0, -1], [0, 0, -1, 1]])
    assert A.analytic_func(exp(x), x) == A.exp()
    raises(ValueError, lambda : A.analytic_func(sqrt(x), x))

    A = Matrix([[41, 12],[12, 34]])
    assert simplify(A.analytic_func(sqrt(x), x)**2) == A

    A = Matrix([[3, -12, 4], [-1, 0, -2], [-1, 5, -1]])
    assert simplify(A.analytic_func(nthroot(x, 3), x)**3) == A

    A = Matrix([[2, 0, 0, 0], [1, 2, 0, 0], [0, 1, 3, 0], [0, 0, 1, 3]])
    assert A.analytic_func(exp(x), x) == A.exp()

    A = Matrix([[0, 2, 1, 6], [0, 0, 1, 2], [0, 0, 0, 3], [0, 0, 0, 0]])
    assert A.analytic_func(exp(x*t), x) == expand(simplify((A*t).exp()))

