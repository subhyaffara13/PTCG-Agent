
def test_particle_compatibility():
    m, l = symbols('m l')
    C_frame = ReferenceFrame('C')
    P = Particle('P')
    C = Particle('C', mass=m)
    q, u = dynamicsymbols('q, u')
    J = PinJoint('J', P, C, q, u, child_interframe=C_frame,
                 child_point=l * C_frame.y)
    assert J.child_interframe == C_frame
    assert J.parent_interframe.name == 'J_P_frame'
    assert C.masscenter.pos_from(P.masscenter) == -l * C_frame.y
    assert C_frame.dcm(J.parent_interframe) == Matrix([[1, 0, 0],
                                                       [0, cos(q), sin(q)],
                                                       [0, -sin(q), cos(q)]])
    assert C.masscenter.vel(J.parent_interframe) == -l * u * C_frame.z
    # Test with specified joint axis
    P_frame = ReferenceFrame('P')
    C_frame = ReferenceFrame('C')
    P = Particle('P')
    C = Particle('C', mass=m)
    q, u = dynamicsymbols('q, u')
    J = PinJoint('J', P, C, q, u, parent_interframe=P_frame,
                 child_interframe=C_frame, child_point=l * C_frame.y,
                 joint_axis=P_frame.z)
    assert J.joint_axis == J.parent_interframe.z
    assert C_frame.dcm(J.parent_interframe) == Matrix([[cos(q), sin(q), 0],
                                                       [-sin(q), cos(q), 0],
                                                       [0, 0, 1]])
    assert P.masscenter.vel(J.parent_interframe) == 0
    assert C.masscenter.vel(J.parent_interframe) == l * u * C_frame.x
    q1, q2, q3, u1, u2, u3 = dynamicsymbols('q1:4 u1:4')
    qdot_to_u = {qi.diff(t): ui for qi, ui in ((q1, u1), (q2, u2), (q3, u3))}
    # Test compatibility for prismatic joint
    P, C = Particle('P'), Particle('C')
    J = PrismaticJoint('J', P, C, q, u)
    assert J.parent_interframe.dcm(J.child_interframe) == eye(3)
    assert C.masscenter.pos_from(P.masscenter) == q * J.parent_interframe.x
    assert P.masscenter.vel(J.parent_interframe) == 0
    assert C.masscenter.vel(J.parent_interframe) == u * J.parent_interframe.x
    # Test compatibility for cylindrical joint
    P, C = Particle('P'), Particle('C')
    P_frame = ReferenceFrame('P_frame')
    J = CylindricalJoint('J', P, C, q1, q2, u1, u2, parent_interframe=P_frame,
                         parent_point=l * P_frame.x, joint_axis=P_frame.y)
    assert J.parent_interframe.dcm(J.child_interframe) == Matrix([
        [cos(q1), 0, sin(q1)], [0, 1, 0], [-sin(q1), 0, cos(q1)]])
    assert C.masscenter.pos_from(P.masscenter) == l * P_frame.x + q2 * P_frame.y
    assert C.masscenter.vel(J.parent_interframe) == u2 * P_frame.y
    assert P.masscenter.vel(J.child_interframe).xreplace(qdot_to_u) == (
        -u2 * P_frame.y - l * u1 * P_frame.z)
    # Test compatibility for planar joint
    P, C = Particle('P'), Particle('C')
    C_frame = ReferenceFrame('C_frame')
    J = PlanarJoint('J', P, C, q1, [q2, q3], u1, [u2, u3],
                    child_interframe=C_frame, child_point=l * C_frame.z)
    P_frame = J.parent_interframe
    assert J.parent_interframe.dcm(J.child_interframe) == Matrix([
        [1, 0, 0], [0, cos(q1), -sin(q1)], [0, sin(q1), cos(q1)]])
    assert C.masscenter.pos_from(P.masscenter) == (
        -l * C_frame.z + q2 * P_frame.y + q3 * P_frame.z)
    assert C.masscenter.vel(J.parent_interframe) == (
        l * u1 * C_frame.y + u2 * P_frame.y + u3 * P_frame.z)
    # Test compatibility for weld joint
    P, C = Particle('P'), Particle('C')
    C_frame, P_frame = ReferenceFrame('C_frame'), ReferenceFrame('P_frame')
    J = WeldJoint('J', P, C, parent_interframe=P_frame,
                  child_interframe=C_frame, parent_point=l * P_frame.x,
                  child_point=l * C_frame.y)
    assert P_frame.dcm(C_frame) == eye(3)
    assert C.masscenter.pos_from(P.masscenter) == l * P_frame.x - l * C_frame.y
    assert C.masscenter.vel(J.parent_interframe) == 0

