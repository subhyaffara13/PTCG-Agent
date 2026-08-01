
def test_orient_space_advanced():
    # space fixed is in the end like body fixed only in opposite order
    q1, q2, q3 = dynamicsymbols('q1:4')
    c1, c2, c3 = symbols('c1:4')
    u1, u2, u3 = dynamicsymbols('q1:4', 1)

    # Test with everything as dynamicsymbols
    A, B = ReferenceFrame('A'), ReferenceFrame('B')
    B.orient_space_fixed(A, (q3, q2, q1), 'yxz')
    assert A.dcm(B) == Matrix([
        [-sin(q1) * sin(q2) * sin(q3) + cos(q1) * cos(q3), -sin(q1) * cos(q2),
         sin(q1) * sin(q2) * cos(q3) + sin(q3) * cos(q1)],
        [sin(q1) * cos(q3) + sin(q2) * sin(q3) * cos(q1), cos(q1) * cos(q2),
         sin(q1) * sin(q3) - sin(q2) * cos(q1) * cos(q3)],
        [-sin(q3) * cos(q2), sin(q2), cos(q2) * cos(q3)]])
    assert B.ang_vel_in(A).to_matrix(B) == Matrix([
        [-sin(q3) * cos(q2) * u1 + cos(q3) * u2],
        [sin(q2) * u1 + u3],
        [sin(q3) * u2 + cos(q2) * cos(q3) * u1]])

    # Test with constant symbol
    A, B = ReferenceFrame('A'), ReferenceFrame('B')
    B.orient_space_fixed(A, (q3, c2, q1), 131)
    assert A.dcm(B) == Matrix([
        [cos(c2), -sin(c2) * cos(q3), sin(c2) * sin(q3)],
        [sin(c2) * cos(q1), -sin(q1) * sin(q3) + cos(c2) * cos(q1) * cos(q3),
         -sin(q1) * cos(q3) - sin(q3) * cos(c2) * cos(q1)],
        [sin(c2) * sin(q1), sin(q1) * cos(c2) * cos(q3) + sin(q3) * cos(q1),
         -sin(q1) * sin(q3) * cos(c2) + cos(q1) * cos(q3)]])
    assert B.ang_vel_in(A).to_matrix(B) == Matrix([
        [cos(c2) * u1 + u3],
        [-sin(c2) * cos(q3) * u1],
        [sin(c2) * sin(q3) * u1]])

    # Test all symbols not time dependent
    A, B = ReferenceFrame('A'), ReferenceFrame('B')
    B.orient_space_fixed(A, (c1, c2, c3), 123)
    assert B.ang_vel_in(A) == Vector(0)

