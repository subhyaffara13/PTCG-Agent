import re

def test_functions():
    one_var = (acosh, ln, Heaviside, factorial, bernoulli, coth, tanh,
            sign, arg, asin, DiracDelta, re, Abs, sinh, cos, cot, acos, acot,
            gamma, bell, harmonic, LambertW, zeta, log, factorial, asinh,
            acoth, cosh, dirichlet_eta, loggamma, erf, ceiling, im, fibonacci,
            tribonacci, conjugate, tan, floor, atanh, sin, atan, lucas, exp)
    two_var = (rf, ff, lowergamma, chebyshevu, chebyshevt, binomial,
            atan2, polygamma, hermite, legendre, uppergamma)
    x, y, z = symbols("x,y,z")
    others = (chebyshevt_root, chebyshevu_root, Eijk(x, y, z),
            Piecewise( (0, x < -1), (x**2, x <= 1), (x**3, True)),
            assoc_legendre)
    for cls in one_var:
        check(cls)
        c = cls(x)
        check(c)
    for cls in two_var:
        check(cls)
        c = cls(x, y)
        check(c)
    for cls in others:
        check(cls)


def test_functions():
    assert residue(1/sin(x), x, 0) == 1
    assert residue(2/sin(x), x, 0) == 2
    assert residue(1/sin(x)**2, x, 0) == 0
    assert residue(1/sin(x)**5, x, 0) == Rational(3, 8)


def test_functions():
    from sympy.core.function import WildFunction
    x = Symbol('x')
    g = WildFunction('g')
    p = Wild('p')
    q = Wild('q')

    f = cos(5*x)
    notf = x
    assert f.match(p*cos(q*x)) == {p: 1, q: 5}
    assert f.match(p*g) == {p: 1, g: cos(5*x)}
    assert notf.match(g) is None


def test_functions():
    dumped_func_a = dill.dumps(function_a)
    assert dill.loads(dumped_func_a)(0) == 0

    dumped_func_b = dill.dumps(function_b)
    assert dill.loads(dumped_func_b)(1,2) == 3

    dumped_func_c = dill.dumps(function_c)
    assert dill.loads(dumped_func_c)(1) == 2
    assert dill.loads(dumped_func_c)(1, 2) == 3

    dumped_func_d = dill.dumps(function_d)
    assert dill.loads(dumped_func_d).__doc__ == function_d.__doc__
    assert dill.loads(dumped_func_d).__module__ == function_d.__module__
    assert dill.loads(dumped_func_d)(1, 2) == 4
    assert dill.loads(dumped_func_d)(1, 2, 3) == 6
    assert dill.loads(dumped_func_d)(1, 2, d2=3) == 6

    function_with_cache(1)
    globalvar = 0
    dumped_func_cache = dill.dumps(function_with_cache)
    assert function_with_cache(2) == 3
    assert function_with_cache(1) == 1
    assert function_with_cache(3) == 6
    assert function_with_cache(2) == 3

    empty_cell = function_with_unassigned_variable()
    cell_copy = dill.loads(dill.dumps(empty_cell))
    assert 'empty' in str(cell_copy.__closure__[0])
    try:
        cell_copy()
    except Exception:
        # this is good
        pass
    else:
        raise AssertionError('cell_copy() did not read an empty cell')

    exec('''
dumped_func_e = dill.dumps(function_e)
assert dill.loads(dumped_func_e)(1, 2) == 6
assert dill.loads(dumped_func_e)(1, 2, 3) == 9
assert dill.loads(dumped_func_e)(1, 2, e2=3) == 8
assert dill.loads(dumped_func_e)(1, 2, e2=3, e3=4) == 10
assert dill.loads(dumped_func_e)(1, 2, 3, e2=4) == 12
assert dill.loads(dumped_func_e)(1, 2, 3, e2=4, e3=5) == 15''')

