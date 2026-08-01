
def test_sympy__matrices__matrixbase__DeferredVector():
    from sympy.matrices.matrixbase import DeferredVector
    assert _test_args(DeferredVector("X"))

