
def test_dcm_diff_16824():
    # NOTE : This is a regression test for the bug introduced in PR 14758,
    # identified in 16824, and solved by PR 16828.

    # This is the solution to Problem 2.2 on page 264 in Kane & Lenvinson's
    # 1985 book.

    q1, q2, q3 = dynamicsymbols('q1:4')

    s1 = sin(q1)
    c1 = cos(q1)
    s2 = sin(q2)
    c2 = cos(q2)
    s3 = sin(q3)
    c3 = cos(q3)

    dcm = Matrix([[c2*c3, s1*s2*c3 - s3*c1, c1*s2*c3 + s3*s1],
                  [c2*s3, s1*s2*s3 + c3*c1, c1*s2*s3 - c3*s1],
                  [-s2,   s1*c2,            c1*c2]])

    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    B.orient(A, 'DCM', dcm)

    AwB = B.ang_vel_in(A)

    alpha2 = s3*c2*q1.diff() + c3*q2.diff()
    beta2 = s1*c2*q3.diff() + c1*q2.diff()

    assert simplify(AwB.dot(A.y) - alpha2) == 0
    assert simplify(AwB.dot(B.y) - beta2) == 0

