
def test_spherical_joint_orient_space():
    q0, q1, q2, u0, u1, u2 = dynamicsymbols('q0:3, u0:3')
    N_R_A = Matrix([
        [-sin(q0) * sin(q2) - sin(q1) * cos(q0) * cos(q2),
         sin(q0) * sin(q1) * cos(q2) - sin(q2) * cos(q0), cos(q1) * cos(q2)],
        [-sin(q0) * cos(q2) + sin(q1) * sin(q2) * cos(q0),
         -sin(q0) * sin(q1) * sin(q2) - cos(q0) * cos(q2), -sin(q2) * cos(q1)],
        [cos(q0) * cos(q1), -sin(q0) * cos(q1), sin(q1)]])
    N_w_A = Matrix([
        [u1 * sin(q0) - u2 * cos(q0) * cos(q1)],
        [u1 * cos(q0) + u2 * sin(q0) * cos(q1)], [u0 - u2 * sin(q1)]])
    N_v_Co = Matrix([
        [u0 - u2 * sin(q1)], [u0 - u2 * sin(q1)],
        [sqrt(2) * (-u1 * sin(q0 + pi / 4) + u2 * cos(q0 + pi / 4) * cos(q1))]])
    # Test default rot_type='BODY', rot_order=123
    N, A, P, C, Pint, Cint = _generate_body(True)
    S = SphericalJoint('S', P, C, coordinates=[q0, q1, q2], speeds=[u0, u1, u2],
                       parent_point=N.x + N.z, child_point=-A.x + A.y,
                       parent_interframe=Pint, child_interframe=Cint,
                       rot_type='space', rot_order=123)
    assert S._rot_type.upper() == 'SPACE'
    assert S._rot_order == 123
    assert simplify(N.dcm(A) - N_R_A) == zeros(3)
    assert simplify(A.ang_vel_in(N).to_matrix(A)) == N_w_A
    assert simplify(C.masscenter.vel(N).to_matrix(A)) == N_v_Co
    # Test change of amounts
    switch_order = lambda expr: expr.xreplace(
        {q0: q1, q1: q0, q2: q2, u0: u1, u1: u0, u2: u2})
    N, A, P, C, Pint, Cint = _generate_body(True)
    S = SphericalJoint('S', P, C, coordinates=[q0, q1, q2], speeds=[u0, u1, u2],
                       parent_point=N.x + N.z, child_point=-A.x + A.y,
                       parent_interframe=Pint, child_interframe=Cint,
                       rot_type='SPACE', amounts=(q1, q0, q2), rot_order=123)
    assert S._rot_type.upper() == 'SPACE'
    assert S._rot_order == 123
    assert simplify(N.dcm(A) - switch_order(N_R_A)) == zeros(3)
    assert simplify(A.ang_vel_in(N).to_matrix(A)) == switch_order(N_w_A)
    assert simplify(C.masscenter.vel(N).to_matrix(A)) == switch_order(N_v_Co)
    # Test different rot_order
    N, A, P, C, Pint, Cint = _generate_body(True)
    S = SphericalJoint('S', P, C, coordinates=[q0, q1, q2], speeds=[u0, u1, u2],
                       parent_point=N.x + N.z, child_point=-A.x + A.y,
                       parent_interframe=Pint, child_interframe=Cint,
                       rot_type='SPaCe', rot_order='zxy')
    assert S._rot_type.upper() == 'SPACE'
    assert S._rot_order == 'zxy'
    assert simplify(N.dcm(A) - Matrix([
        [-sin(q2) * cos(q1), -sin(q0) * cos(q2) + sin(q1) * sin(q2) * cos(q0),
         sin(q0) * sin(q1) * sin(q2) + cos(q0) * cos(q2)],
        [-sin(q1), -cos(q0) * cos(q1), -sin(q0) * cos(q1)],
        [cos(q1) * cos(q2), -sin(q0) * sin(q2) - sin(q1) * cos(q0) * cos(q2),
         -sin(q0) * sin(q1) * cos(q2) + sin(q2) * cos(q0)]]))
    assert simplify(A.ang_vel_in(N).to_matrix(A) - Matrix([
        [-u0 + u2 * sin(q1)], [-u1 * sin(q0) + u2 * cos(q0) * cos(q1)],
        [u1 * cos(q0) + u2 * sin(q0) * cos(q1)]])) == zeros(3, 1)
    assert simplify(C.masscenter.vel(N).to_matrix(A) - Matrix([
        [u1 * cos(q0) + u2 * sin(q0) * cos(q1)],
        [u1 * cos(q0) + u2 * sin(q0) * cos(q1)],
        [u0 + u1 * sin(q0) - u2 * sin(q1) -
         u2 * cos(q0) * cos(q1)]])) == zeros(3, 1)

