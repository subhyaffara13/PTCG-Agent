
def test_dot_different_frames():
    assert dot(N.x, A.x) == cos(q1)
    assert dot(N.x, A.y) == -sin(q1)
    assert dot(N.x, A.z) == 0
    assert dot(N.y, A.x) == sin(q1)
    assert dot(N.y, A.y) == cos(q1)
    assert dot(N.y, A.z) == 0
    assert dot(N.z, A.x) == 0
    assert dot(N.z, A.y) == 0
    assert dot(N.z, A.z) == 1

    assert trigsimp(dot(N.x, A.x + A.y)) == sqrt(2)*cos(q1 + pi/4)
    assert trigsimp(dot(N.x, A.x + A.y)) == trigsimp(dot(A.x + A.y, N.x))

    assert dot(A.x, C.x) == cos(q3)
    assert dot(A.x, C.y) == 0
    assert dot(A.x, C.z) == sin(q3)
    assert dot(A.y, C.x) == sin(q2)*sin(q3)
    assert dot(A.y, C.y) == cos(q2)
    assert dot(A.y, C.z) == -sin(q2)*cos(q3)
    assert dot(A.z, C.x) == -cos(q2)*sin(q3)
    assert dot(A.z, C.y) == sin(q2)
    assert dot(A.z, C.z) == cos(q2)*cos(q3)

