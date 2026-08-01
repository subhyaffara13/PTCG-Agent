
def test_tensor_alternative_construction():
    L = TensorIndexType("L")
    i0, i1, i2, i3 = tensor_indices('i0:4', L)
    A = TensorHead("A", [L])
    x, y = symbols("x y")

    assert A(i0) == A(Symbol("i0"))
    assert A(-i0) == A(-Symbol("i0"))
    raises(TypeError, lambda: A(x+y))
    raises(ValueError, lambda: A(2*x))

