
def test_kin_eqs():
    q0, q1, q2, q3 = dynamicsymbols('q0 q1 q2 q3')
    q0d, q1d, q2d, q3d = dynamicsymbols('q0 q1 q2 q3', 1)
    u1, u2, u3 = dynamicsymbols('u1 u2 u3')
    ke = kinematic_equations([u1,u2,u3], [q1,q2,q3], 'body', 313)
    assert ke == kinematic_equations([u1,u2,u3], [q1,q2,q3], 'body', '313')
    kds = kinematic_equations([u1, u2, u3], [q0, q1, q2, q3], 'quaternion')
    assert kds == [-0.5 * q0 * u1 - 0.5 * q2 * u3 + 0.5 * q3 * u2 + q1d,
            -0.5 * q0 * u2 + 0.5 * q1 * u3 - 0.5 * q3 * u1 + q2d,
            -0.5 * q0 * u3 - 0.5 * q1 * u2 + 0.5 * q2 * u1 + q3d,
            0.5 * q1 * u1 + 0.5 * q2 * u2 + 0.5 * q3 * u3 + q0d]
    raises(ValueError, lambda: kinematic_equations([u1, u2, u3], [q0, q1, q2], 'quaternion'))
    raises(ValueError, lambda: kinematic_equations([u1, u2, u3], [q0, q1, q2, q3], 'quaternion', '123'))
    raises(ValueError, lambda: kinematic_equations([u1, u2, u3], [q0, q1, q2, q3], 'foo'))
    raises(TypeError, lambda: kinematic_equations(u1, [q0, q1, q2, q3], 'quaternion'))
    raises(TypeError, lambda: kinematic_equations([u1], [q0, q1, q2, q3], 'quaternion'))
    raises(TypeError, lambda: kinematic_equations([u1, u2, u3], q0, 'quaternion'))
    raises(ValueError, lambda: kinematic_equations([u1, u2, u3], [q0, q1, q2, q3], 'body'))
    raises(ValueError, lambda: kinematic_equations([u1, u2, u3], [q0, q1, q2, q3], 'space'))
    raises(ValueError, lambda: kinematic_equations([u1, u2, u3], [q0, q1, q2], 'body', '222'))
    assert kinematic_equations([0, 0, 0], [q0, q1, q2], 'space') == [S.Zero, S.Zero, S.Zero]

