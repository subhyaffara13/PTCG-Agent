
def test_sympy__algebras__quaternion__Quaternion():
    from sympy.algebras.quaternion import Quaternion
    assert _test_args(Quaternion(x, 1, 2, 3))

