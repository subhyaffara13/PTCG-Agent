
def test_matrix_solve_derivative_numpy():
    np = import_module('numpy')
    if not np:
        skip("numpy not installed.")
    q = symbols('q')
    a11, a12, a21, a22, b1, b2 = (
        f(q) for f in symbols('a11 a12 a21 a22 b1 b2', cls=Function))
    A = Matrix([[a11, a12], [a21, a22]])
    b = Matrix([b1, b2])
    dx_lu = A.LUsolve(b).diff(q)
    subs = {a11.diff(q): 0.2, a12.diff(q): 0.3, a21.diff(q): 0.1,
            a22.diff(q): 0.5, b1.diff(q): 0.4, b2.diff(q): 0.9,
            a11: 1.3, a12: 0.5, a21: 1.2, a22: 4, b1: 6.2, b2: 3.5}
    p, p_vals = zip(*subs.items())
    dx_sm = MatrixSolve(A, b).diff(q)
    np.testing.assert_allclose(
        lambdify(p, dx_sm, printer=NumPyPrinter)(*p_vals),
        lambdify(p, dx_lu, printer=NumPyPrinter)(*p_vals))

