
def test_jordan_form_issue_15858():
    A = Matrix([
        [1, 1, 1, 0],
        [-2, -1, 0, -1],
        [0, 0, -1, -1],
        [0, 0, 2, 1]])
    (P, J) = A.jordan_form()
    assert P.expand() == Matrix([
        [    -I,          -I/2,      I,           I/2],
        [-1 + I,             0, -1 - I,             0],
        [     0, -S(1)/2 - I/2,      0, -S(1)/2 + I/2],
        [     0,             1,      0,             1]])
    assert J == Matrix([
        [-I, 1, 0, 0],
        [0, -I, 0, 0],
        [0, 0, I, 1],
        [0, 0, 0, I]])


def test_jordan_form_issue_15858():
    A = Matrix([
        [1, 1, 1, 0],
        [-2, -1, 0, -1],
        [0, 0, -1, -1],
        [0, 0, 2, 1]])
    (P, J) = A.jordan_form()
    assert P.expand() == Matrix([
        [    -I,          -I/2,      I,           I/2],
        [-1 + I,             0, -1 - I,             0],
        [     0, -S(1)/2 - I/2,      0, -S(1)/2 + I/2],
        [     0,             1,      0,             1]])
    assert J == Matrix([
        [-I, 1, 0, 0],
        [0, -I, 0, 0],
        [0, 0, I, 1],
        [0, 0, 0, I]])

