
def test_vector_dot():
    assert i.dot(Vector.zero) == 0
    assert Vector.zero.dot(i) == 0
    assert i & Vector.zero == 0

    assert i.dot(i) == 1
    assert i.dot(j) == 0
    assert i.dot(k) == 0
    assert i & i == 1
    assert i & j == 0
    assert i & k == 0

    assert j.dot(i) == 0
    assert j.dot(j) == 1
    assert j.dot(k) == 0
    assert j & i == 0
    assert j & j == 1
    assert j & k == 0

    assert k.dot(i) == 0
    assert k.dot(j) == 0
    assert k.dot(k) == 1
    assert k & i == 0
    assert k & j == 0
    assert k & k == 1

    raises(TypeError, lambda: k.dot(1))

