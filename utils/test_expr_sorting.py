
def test_expr_sorting():

    exprs = [1/x**2, 1/x, sqrt(sqrt(x)), sqrt(x), x, sqrt(x)**3, x**2]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [x, 2*x, 2*x**2, 2*x**3, x**n, 2*x**n, sin(x), sin(x)**n,
             sin(x**2), cos(x), cos(x**2), tan(x)]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [x + 1, x**2 + x + 1, x**3 + x**2 + x + 1]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [S(4), x - 3*I/2, x + 3*I/2, x - 4*I + 1, x + 4*I + 1]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [f(1), f(2), f(3), f(1, 2, 3), g(1), g(2), g(3), g(1, 2, 3)]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [f(x), g(x), exp(x), sin(x), cos(x), factorial(x)]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [Tuple(x, y), Tuple(x, z), Tuple(x, y, z)]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [[3], [1, 2]]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [[1, 2], [2, 3]]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [[1, 2], [1, 2, 3]]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [{x: -y}, {x: y}]
    assert sorted(exprs, key=default_sort_key) == exprs

    exprs = [{1}, {1, 2}]
    assert sorted(exprs, key=default_sort_key) == exprs

    a, b = exprs = [Dummy('x'), Dummy('x')]
    assert sorted([b, a], key=default_sort_key) == exprs

