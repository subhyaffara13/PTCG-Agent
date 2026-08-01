
def test_sympy__physics__units__quantities__Quantity():
    from sympy.physics.units.quantities import Quantity
    assert _test_args(Quantity("dam"))

