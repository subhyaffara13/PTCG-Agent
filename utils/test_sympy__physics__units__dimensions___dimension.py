
def test_sympy__physics__units__dimensions__Dimension():
    from sympy.physics.units.dimensions import Dimension
    assert _test_args(Dimension("length", "L"))

