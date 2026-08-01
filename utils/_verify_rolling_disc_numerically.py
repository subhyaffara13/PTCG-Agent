
def _verify_rolling_disc_numerically(kane, all_zero=False):
    q, u, p = dynamicsymbols('q1:6'), dynamicsymbols('u1:6'), symbols('g r m')
    eval_sys = lambdify((q, u, p), (kane.mass_matrix_full, kane.forcing_full),
                        cse=True)
    solve_sys = lambda q, u, p: Matrix.LUsolve(
        *(Matrix(mat) for mat in eval_sys(q, u, p)))
    solve_u_dep = lambdify((q, u[:3], p), kane._Ars * Matrix(u[:3]), cse=True)
    eps = 1e-10
    p_vals = (9.81, 0.26, 3.43)
    # First numeric test
    q_vals = (0.3, 0.1, 1.97, -0.35, 2.27)
    u_vals = [-0.2, 1.3, 0.15]
    u_vals.extend(solve_u_dep(q_vals, u_vals, p_vals)[:2, 0])
    expected = Matrix([
        0.126603940595934, 0.215942571601660, 1.28736069604936,
        0.319764288376543, 0.0989146857254898, -0.925848952664489,
        -0.0181350656532944, 2.91695398184589, -0.00992793421754526,
        0.0412861634829171])
    assert all(abs(x) < eps for x in
               (solve_sys(q_vals, u_vals, p_vals) - expected))
    # Second numeric test
    q_vals = (3.97, -0.28, 8.2, -0.35, 2.27)
    u_vals = [-0.25, -2.2, 0.62]
    u_vals.extend(solve_u_dep(q_vals, u_vals, p_vals)[:2, 0])
    expected = Matrix([
        0.0259159090798597, 0.668041660387416, -2.19283799213811,
        0.385441810852219, 0.420109283790573, 1.45030568179066,
        -0.0110924422400793, -8.35617840186040, -0.154098542632173,
        -0.146102664410010])
    assert all(abs(x) < eps for x in
               (solve_sys(q_vals, u_vals, p_vals) - expected))
    if all_zero:
        q_vals = (0, 0, 0, 0, 0)
        u_vals = (0, 0, 0, 0, 0)
        assert solve_sys(q_vals, u_vals, p_vals) == zeros(10, 1)

