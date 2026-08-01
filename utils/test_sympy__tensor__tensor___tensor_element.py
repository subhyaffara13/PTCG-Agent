
def test_sympy__tensor__tensor__TensorElement():
    from sympy.tensor.tensor import TensorIndexType, TensorHead, TensorElement
    L = TensorIndexType("L")
    A = TensorHead("A", [L, L])
    telem = TensorElement(A(x, y), {x: 1})
    assert _test_args(telem)

