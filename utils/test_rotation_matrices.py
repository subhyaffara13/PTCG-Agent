
def test_rotation_matrices():
    # This tests the rotation matrices by rotating about an axis and back.
    theta = pi/3
    r3_plus = rot_axis3(theta)
    r3_minus = rot_axis3(-theta)
    r2_plus = rot_axis2(theta)
    r2_minus = rot_axis2(-theta)
    r1_plus = rot_axis1(theta)
    r1_minus = rot_axis1(-theta)
    assert r3_minus*r3_plus*eye(3) == eye(3)
    assert r2_minus*r2_plus*eye(3) == eye(3)
    assert r1_minus*r1_plus*eye(3) == eye(3)

    # Check the correctness of the trace of the rotation matrix
    assert r1_plus.trace() == 1 + 2*cos(theta)
    assert r2_plus.trace() == 1 + 2*cos(theta)
    assert r3_plus.trace() == 1 + 2*cos(theta)

    # Check that a rotation with zero angle doesn't change anything.
    assert rot_axis1(0) == eye(3)
    assert rot_axis2(0) == eye(3)
    assert rot_axis3(0) == eye(3)

    # Check left-hand convention
    # see Issue #24529
    q1 = Quaternion.from_axis_angle([1, 0, 0], pi / 2)
    q2 = Quaternion.from_axis_angle([0, 1, 0], pi / 2)
    q3 = Quaternion.from_axis_angle([0, 0, 1], pi / 2)
    assert rot_axis1(- pi / 2) == q1.to_rotation_matrix()
    assert rot_axis2(- pi / 2) == q2.to_rotation_matrix()
    assert rot_axis3(- pi / 2) == q3.to_rotation_matrix()
    # Check right-hand convention
    assert rot_ccw_axis1(+ pi / 2) == q1.to_rotation_matrix()
    assert rot_ccw_axis2(+ pi / 2) == q2.to_rotation_matrix()
    assert rot_ccw_axis3(+ pi / 2) == q3.to_rotation_matrix()


def test_rotation_matrices():
    # This tests the rotation matrices by rotating about an axis and back.
    theta = pi/3
    r3_plus = rot_axis3(theta)
    r3_minus = rot_axis3(-theta)
    r2_plus = rot_axis2(theta)
    r2_minus = rot_axis2(-theta)
    r1_plus = rot_axis1(theta)
    r1_minus = rot_axis1(-theta)
    assert r3_minus*r3_plus*eye(3) == eye(3)
    assert r2_minus*r2_plus*eye(3) == eye(3)
    assert r1_minus*r1_plus*eye(3) == eye(3)

    # Check the correctness of the trace of the rotation matrix
    assert r1_plus.trace() == 1 + 2*cos(theta)
    assert r2_plus.trace() == 1 + 2*cos(theta)
    assert r3_plus.trace() == 1 + 2*cos(theta)

    # Check that a rotation with zero angle doesn't change anything.
    assert rot_axis1(0) == eye(3)
    assert rot_axis2(0) == eye(3)
    assert rot_axis3(0) == eye(3)

    # Check left-hand convention
    # see Issue #24529
    q1 = Quaternion.from_axis_angle([1, 0, 0], pi / 2)
    q2 = Quaternion.from_axis_angle([0, 1, 0], pi / 2)
    q3 = Quaternion.from_axis_angle([0, 0, 1], pi / 2)
    assert rot_axis1(- pi / 2) == q1.to_rotation_matrix()
    assert rot_axis2(- pi / 2) == q2.to_rotation_matrix()
    assert rot_axis3(- pi / 2) == q3.to_rotation_matrix()
    # Check right-hand convention
    assert rot_ccw_axis1(+ pi / 2) == q1.to_rotation_matrix()
    assert rot_ccw_axis2(+ pi / 2) == q2.to_rotation_matrix()
    assert rot_ccw_axis3(+ pi / 2) == q3.to_rotation_matrix()

