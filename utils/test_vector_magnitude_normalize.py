
def test_vector_magnitude_normalize():
    assert Vector.zero.magnitude() == 0
    assert Vector.zero.normalize() == Vector.zero

    assert i.magnitude() == 1
    assert j.magnitude() == 1
    assert k.magnitude() == 1
    assert i.normalize() == i
    assert j.normalize() == j
    assert k.normalize() == k

    v1 = a * i
    assert v1.normalize() == (a/sqrt(a**2))*i
    assert v1.magnitude() == sqrt(a**2)

    v2 = a*i + b*j + c*k
    assert v2.magnitude() == sqrt(a**2 + b**2 + c**2)
    assert v2.normalize() == v2 / v2.magnitude()

    v3 = i + j
    assert v3.normalize() == (sqrt(2)/2)*C.i + (sqrt(2)/2)*C.j

