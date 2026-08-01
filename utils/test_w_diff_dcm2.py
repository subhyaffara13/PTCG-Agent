
def test_w_diff_dcm2():
    q1, q2, q3 = dynamicsymbols('q1:4')
    N = ReferenceFrame('N')
    A = N.orientnew('A', 'axis', [q1, N.x])
    B = A.orientnew('B', 'axis', [q2, A.y])
    C = B.orientnew('C', 'axis', [q3, B.z])

    DCM = C.dcm(N).T
    D = N.orientnew('D', 'DCM', DCM)

    # Frames D and C are the same ReferenceFrame,
    # since they have equal DCM respect to frame N.
    # Therefore, D and C should have same angle velocity in N.
    assert D.dcm(N) == C.dcm(N) == Matrix([
        [cos(q2)*cos(q3), sin(q1)*sin(q2)*cos(q3) +
        sin(q3)*cos(q1), sin(q1)*sin(q3) -
        sin(q2)*cos(q1)*cos(q3)], [-sin(q3)*cos(q2),
        -sin(q1)*sin(q2)*sin(q3) + cos(q1)*cos(q3),
        sin(q1)*cos(q3) + sin(q2)*sin(q3)*cos(q1)],
        [sin(q2), -sin(q1)*cos(q2), cos(q1)*cos(q2)]])
    assert (D.ang_vel_in(N) - C.ang_vel_in(N)).express(N).simplify() == 0

