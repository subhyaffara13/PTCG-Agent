
def test_body_dcm():
    with warns_deprecated_sympy():
        A = Body('A')
        B = Body('B')
    A.frame.orient_axis(B.frame, B.frame.z, 10)
    assert A.dcm(B) == Matrix([[cos(10), sin(10), 0], [-sin(10), cos(10), 0], [0, 0, 1]])
    assert A.dcm(B.frame) == Matrix([[cos(10), sin(10), 0], [-sin(10), cos(10), 0], [0, 0, 1]])

