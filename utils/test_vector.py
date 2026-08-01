
def test_vector(doc):
    """std::vector <-> list"""
    lst = m.cast_vector()
    assert lst == [1]
    lst.append(2)
    assert m.load_vector(lst)
    assert m.load_vector(tuple(lst))

    assert m.cast_bool_vector() == [True, False]
    assert m.load_bool_vector([True, False])
    assert m.load_bool_vector((True, False))

    assert doc(m.cast_vector) == "cast_vector() -> List[int]"
    assert doc(m.load_vector) == "load_vector(arg0: List[int]) -> bool"

    # Test regression caused by 936: pointers to stl containers weren't castable
    assert m.cast_ptr_vector() == ["lvalue", "lvalue"]


def test_vector():
    assert isinstance(i, BaseVector)
    assert i != j
    assert j != k
    assert k != i
    assert i - i == Vector.zero
    assert i + Vector.zero == i
    assert i - Vector.zero == i
    assert Vector.zero != 0
    assert -Vector.zero == Vector.zero

    v1 = a*i + b*j + c*k
    v2 = a**2*i + b**2*j + c**2*k
    v3 = v1 + v2
    v4 = 2 * v1
    v5 = a * i

    assert isinstance(v1, VectorAdd)
    assert v1 - v1 == Vector.zero
    assert v1 + Vector.zero == v1
    assert v1.dot(i) == a
    assert v1.dot(j) == b
    assert v1.dot(k) == c
    assert i.dot(v2) == a**2
    assert j.dot(v2) == b**2
    assert k.dot(v2) == c**2
    assert v3.dot(i) == a**2 + a
    assert v3.dot(j) == b**2 + b
    assert v3.dot(k) == c**2 + c

    assert v1 + v2 == v2 + v1
    assert v1 - v2 == -1 * (v2 - v1)
    assert a * v1 == v1 * a

    assert isinstance(v5, VectorMul)
    assert v5.base_vector == i
    assert v5.measure_number == a
    assert isinstance(v4, Vector)
    assert isinstance(v4, VectorAdd)
    assert isinstance(v4, Vector)
    assert isinstance(Vector.zero, VectorZero)
    assert isinstance(Vector.zero, Vector)
    assert isinstance(v1 * 0, VectorZero)

    assert v1.to_matrix(C) == Matrix([[a], [b], [c]])

    assert i.components == {i: 1}
    assert v5.components == {i: a}
    assert v1.components == {i: a, j: b, k: c}

    assert VectorAdd(v1, Vector.zero) == v1
    assert VectorMul(a, v1) == v1*a
    assert VectorMul(1, i) == i
    assert VectorAdd(v1, Vector.zero) == v1
    assert VectorMul(0, Vector.zero) == Vector.zero
    raises(TypeError, lambda: v1.outer(1))
    raises(TypeError, lambda: v1.dot(1))


def test_vector():
    x = matrix([0, 1, 2, 3, 4])
    assert x == matrix([[0], [1], [2], [3], [4]])
    assert x[3] == 3
    assert len(x._matrix__data) == 4
    assert list(x) == list(range(5))
    x[0] = -10
    x[4] = 0
    assert x[0] == -10
    assert len(x) == len(x.T) == 5
    assert x.T*x == matrix([[114]])

