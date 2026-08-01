
def test_python_matrix():
    p = python(Matrix([[x**2+1, 1], [y, x+y]]))
    s = "x = Symbol('x')\ny = Symbol('y')\ne = MutableDenseMatrix([[x**2 + 1, 1], [y, x + y]])"
    assert p == s

