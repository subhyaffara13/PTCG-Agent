
def test_rigid_body_particle_compatibility():
    l, m, g = symbols('l m g')
    C = RigidBody('C')
    b = Particle('b', mass=m)
    b_frame = ReferenceFrame('b_frame')
    q, u = dynamicsymbols('q u')
    P = PinJoint('P', C, b, coordinates=q, speeds=u, child_interframe=b_frame,
                 child_point=-l * b_frame.x, joint_axis=C.z)
    with warns_deprecated_sympy():
        method = JointsMethod(C, P)
    method.loads.append((b.masscenter, m * g * C.x))
    method.form_eoms()
    rhs = method.rhs()
    assert rhs[1] == -g*sin(q)/l

