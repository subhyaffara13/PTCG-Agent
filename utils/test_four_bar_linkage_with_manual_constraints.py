
def test_four_bar_linkage_with_manual_constraints():
    q1, q2, q3, u1, u2, u3 = dynamicsymbols('q1:4, u1:4')
    l1, l2, l3, l4, rho = symbols('l1:5, rho')

    N = ReferenceFrame('N')
    inertias = [inertia(N, 0, 0, rho * l ** 3 / 12) for l in (l1, l2, l3, l4)]
    with warns_deprecated_sympy():
        link1 = Body('Link1', frame=N, mass=rho * l1,
                     central_inertia=inertias[0])
        link2 = Body('Link2', mass=rho * l2, central_inertia=inertias[1])
        link3 = Body('Link3', mass=rho * l3, central_inertia=inertias[2])
        link4 = Body('Link4', mass=rho * l4, central_inertia=inertias[3])

    joint1 = PinJoint(
        'J1', link1, link2, coordinates=q1, speeds=u1, joint_axis=link1.z,
        parent_point=l1 / 2 * link1.x, child_point=-l2 / 2 * link2.x)
    joint2 = PinJoint(
        'J2', link2, link3, coordinates=q2, speeds=u2, joint_axis=link2.z,
        parent_point=l2 / 2 * link2.x, child_point=-l3 / 2 * link3.x)
    joint3 = PinJoint(
        'J3', link3, link4, coordinates=q3, speeds=u3, joint_axis=link3.z,
        parent_point=l3 / 2 * link3.x, child_point=-l4 / 2 * link4.x)

    loop = link4.masscenter.pos_from(link1.masscenter) \
           + l1 / 2 * link1.x + l4 / 2 * link4.x

    fh = Matrix([loop.dot(link1.x), loop.dot(link1.y)])

    with warns_deprecated_sympy():
        method = JointsMethod(link1, joint1, joint2, joint3)

    t = dynamicsymbols._t
    qdots = solve(method.kdes, [q1.diff(t), q2.diff(t), q3.diff(t)])
    fhd = fh.diff(t).subs(qdots)

    kane = KanesMethod(method.frame, q_ind=[q1], u_ind=[u1],
                       q_dependent=[q2, q3], u_dependent=[u2, u3],
                       kd_eqs=method.kdes, configuration_constraints=fh,
                       velocity_constraints=fhd, forcelist=method.loads,
                       bodies=method.bodies)
    fr, frs = kane.kanes_equations()
    assert fr == zeros(1)

    # Numerically check the mass- and forcing-matrix
    p = Matrix([l1, l2, l3, l4, rho])
    q = Matrix([q1, q2, q3])
    u = Matrix([u1, u2, u3])
    eval_m = lambdify((q, p), kane.mass_matrix)
    eval_f = lambdify((q, u, p), kane.forcing)
    eval_fhd = lambdify((q, u, p), fhd)

    p_vals = [0.13, 0.24, 0.21, 0.34, 997]
    q_vals = [2.1, 0.6655470375077588, 2.527408138024188]  # Satisfies fh
    u_vals = [0.2, -0.17963733938852067, 0.1309060540601612]  # Satisfies fhd
    mass_check = Matrix([[3.452709815256506e+01, 7.003948798374735e+00,
                          -4.939690970641498e+00],
                         [-2.203792703880936e-14, 2.071702479957077e-01,
                          2.842917573033711e-01],
                         [-1.300000000000123e-01, -8.836934896046506e-03,
                          1.864891330060847e-01]])
    forcing_check = Matrix([[-0.031211821321648],
                            [-0.00066022608181],
                            [0.001813559741243]])
    eps = 1e-10
    assert all(abs(x) < eps for x in eval_fhd(q_vals, u_vals, p_vals))
    assert all(abs(x) < eps for x in
               (Matrix(eval_m(q_vals, p_vals)) - mass_check))
    assert all(abs(x) < eps for x in
               (Matrix(eval_f(q_vals, u_vals, p_vals)) - forcing_check))

