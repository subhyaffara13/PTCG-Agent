
def test_kane_rolling_disc_kdes_callable():
    props = _create_rolling_disc()
    kane = KanesMethod(
        props['frame'], props['q_ind'], props['u_ind'], props['kdes'],
        u_dependent=props['u_dep'], velocity_constraints=props['fnh'],
        bodies=props['bodies'], forcelist=props['loads'],
        explicit_kinematics=False,
        kd_eqs_solver=lambda A, b: simplify(A.LUsolve(b)))
    q, u, p = dynamicsymbols('q1:6'), dynamicsymbols('u1:6'), symbols('g r m')
    qd = dynamicsymbols('q1:6', 1)
    eval_kdes = lambdify((q, qd, u, p), tuple(kane.kindiffdict().items()))
    eps = 1e-10
    # Test with only zeros. If 'LU' would be used this would result in nan.
    p_vals = (9.81, 0.25, 3.5)
    zero_vals = (0, 0, 0, 0, 0)
    assert all(abs(qdi - fui) < eps for qdi, fui in
               eval_kdes(zero_vals, zero_vals, zero_vals, p_vals))
    # Test with some arbitrary values
    q_vals = tuple(map(float, (pi / 6, pi / 3, pi / 2, 0.42, 0.62)))
    qd_vals = tuple(map(float, (4, 1 / 3, 4 - 2 * sqrt(3),
                                0.25 * (2 * sqrt(3) - 3),
                                0.25 * (2 - sqrt(3)))))
    u_vals = tuple(map(float, (-2, 4, 1 / 3, 0.25 * (-3 + 2 * sqrt(3)),
                               0.25 * (-sqrt(3) + 2))))
    assert all(abs(qdi - fui) < eps for qdi, fui in
               eval_kdes(q_vals, qd_vals, u_vals, p_vals))

