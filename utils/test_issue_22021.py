
def test_issue_22021():
    from sympy.calculus.accumulationbounds import AccumBounds
    # these objects are special cases in Mul
    from sympy.tensor.tensor import TensorIndexType, tensor_indices, tensor_heads
    L = TensorIndexType("L")
    i = tensor_indices("i", L)
    A, B = tensor_heads("A B", [L])
    e = A(i) + B(i)
    assert -e == -1*e
    e = zoo + x
    assert -e == -1*e
    a = AccumBounds(1, 2)
    e = a + x
    assert -e == -1*e
    for args in permutations((zoo, a, x)):
        e = Add(*args, evaluate=False)
        assert -e == -1*e
    assert 2*Add(1, x, x, evaluate=False) == 4*x + 2

