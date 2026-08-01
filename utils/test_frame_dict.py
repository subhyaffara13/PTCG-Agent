
def test_frame_dict():
    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    C = ReferenceFrame('C')

    a, b, c = symbols('a b c')

    B.orient_axis(A, A.x, a)
    assert A._dcm_dict == {B: Matrix([[1, 0, 0],[0, cos(a), -sin(a)],[0, sin(a),  cos(a)]])}
    assert B._dcm_dict == {A: Matrix([[1, 0, 0],[0,  cos(a), sin(a)],[0, -sin(a), cos(a)]])}
    assert C._dcm_dict == {}

    B.orient_axis(C, C.x, b)
    # Previous relation is not wiped
    assert A._dcm_dict == {B: Matrix([[1, 0, 0],[0, cos(a), -sin(a)],[0, sin(a),  cos(a)]])}
    assert B._dcm_dict == {A: Matrix([[1, 0, 0],[0,  cos(a), sin(a)],[0, -sin(a), cos(a)]]), \
        C: Matrix([[1, 0, 0],[0,  cos(b), sin(b)],[0, -sin(b), cos(b)]])}
    assert C._dcm_dict == {B: Matrix([[1, 0, 0],[0, cos(b), -sin(b)],[0, sin(b),  cos(b)]])}

    A.orient_axis(B, B.x, c)
    # Previous relation is updated
    assert B._dcm_dict == {C: Matrix([[1, 0, 0],[0,  cos(b), sin(b)],[0, -sin(b), cos(b)]]),\
        A: Matrix([[1, 0, 0],[0, cos(c), -sin(c)],[0, sin(c),  cos(c)]])}
    assert A._dcm_dict == {B: Matrix([[1, 0, 0],[0,  cos(c), sin(c)],[0, -sin(c), cos(c)]])}
    assert C._dcm_dict == {B: Matrix([[1, 0, 0],[0, cos(b), -sin(b)],[0, sin(b),  cos(b)]])}

