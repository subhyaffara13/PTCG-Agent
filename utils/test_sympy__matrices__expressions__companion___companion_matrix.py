
def test_sympy__matrices__expressions__companion__CompanionMatrix():
    from sympy.core.symbol import Symbol
    from sympy.matrices.expressions.companion import CompanionMatrix
    from sympy.polys.polytools import Poly

    x = Symbol('x')
    p = Poly([1, 2, 3], x)
    assert _test_args(CompanionMatrix(p))

