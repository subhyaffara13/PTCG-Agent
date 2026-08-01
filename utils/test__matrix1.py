
def test_Matrix1():
    m = Matrix([[x, x**2], [5, 2/x]])
    assert (array(m.subs(x, 2)) == array([[2, 4], [5, 1]])).all()
    m = Matrix([[sin(x), x**2], [5, 2/x]])
    assert (array(m.subs(x, 2)) == array([[sin(2), 4], [5, 1]])).all()

