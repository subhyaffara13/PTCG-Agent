
def test_numpy_matrix():
    if not numpy:
        skip("numpy not installed.")
    A = Matrix([[x, x*y], [sin(z) + 4, x**z]])
    sol_arr = numpy.array([[1, 2], [numpy.sin(3) + 4, 1]])
    #Lambdify array first, to ensure return to array as default
    f = lambdify((x, y, z), A, ['numpy'])
    numpy.testing.assert_allclose(f(1, 2, 3), sol_arr)
    #Check that the types are arrays and matrices
    assert isinstance(f(1, 2, 3), numpy.ndarray)

    # gh-15071
    class dot(Function):
        pass
    x_dot_mtx = dot(x, Matrix([[2], [1], [0]]))
    f_dot1 = lambdify(x, x_dot_mtx)
    inp = numpy.zeros((17, 3))
    assert numpy.all(f_dot1(inp) == 0)

    strict_kw = {"allow_unknown_functions": False, "inline": True, "fully_qualified_modules": False}
    p2 = NumPyPrinter(dict(user_functions={'dot': 'dot'}, **strict_kw))
    f_dot2 = lambdify(x, x_dot_mtx, printer=p2)
    assert numpy.all(f_dot2(inp) == 0)

    p3 = NumPyPrinter(strict_kw)
    # The line below should probably fail upon construction (before calling with "(inp)"):
    raises(Exception, lambda: lambdify(x, x_dot_mtx, printer=p3)(inp))


def test_numpy_matrix():
    p = NumPyPrinter()
    assert p.doprint(Matrix([[1, 2], [3, 5]])) == 'numpy.array([[1, 2], [3, 5]])'
    assert p.doprint(Matrix([1, 2])) == 'numpy.array([[1], [2]])'
    assert p.doprint(Matrix(0, 0, [])) == 'numpy.zeros((0, 0))'
    assert p.doprint(Matrix(0, 1, [])) == 'numpy.zeros((0, 1))'
    assert p.doprint(Matrix(1, 0, [])) == 'numpy.zeros((1, 0))'

