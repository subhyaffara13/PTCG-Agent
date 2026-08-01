
def test_body_axis():
    N = ReferenceFrame('N')
    with warns_deprecated_sympy():
        B = Body('B', frame=N)
    assert B.x == N.x
    assert B.y == N.y
    assert B.z == N.z

