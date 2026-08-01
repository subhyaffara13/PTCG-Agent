
def test_sympy__physics__units__prefixes__Prefix():
    from sympy.physics.units.prefixes import Prefix
    assert _test_args(Prefix('kilo', 'k', 3))

