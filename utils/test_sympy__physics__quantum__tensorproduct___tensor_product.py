
def test_sympy__physics__quantum__tensorproduct__TensorProduct():
    from sympy.physics.quantum.tensorproduct import TensorProduct
    x, y = symbols("x y", commutative=False)
    assert _test_args(TensorProduct(x, y))

