
def test_vector_sympy():
    """
    Test whether the Vector framework confirms to the hashing
    and equality testing properties of SymPy.
    """
    v1 = 3*j
    assert v1 == j*3
    assert v1.components == {j: 3}
    v2 = 3*i + 4*j + 5*k
    v3 = 2*i + 4*j + i + 4*k + k
    assert v3 == v2
    assert v3.__hash__() == v2.__hash__()

