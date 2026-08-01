
def test_process_cse():
    x, y, z = symbols('x y z')
    f = Function('f')
    k = Function('k')
    expr = Matrix([f(k(x,y), z) + Derivative(f(k(x,y), z), x) + k(x,y) + 2*x])
    repl, reduced = cse(expr)
    p_repl, p_reduced = _remove_cse_from_derivative(repl, reduced)

    x0 = symbols('x0')
    x1 = symbols('x1')

    expected_output = (
        [(x0, k(x, y)), (x1, f(x0, z))],
        [Matrix([2 * x + x0 + x1 + Derivative(f(k(x, y), z), x)])]
    )

    assert p_repl == expected_output[0], f"Expected {expected_output[0]}, but got {p_repl}"
    assert p_reduced == expected_output[1], f"Expected {expected_output[1]}, but got {p_reduced}"

