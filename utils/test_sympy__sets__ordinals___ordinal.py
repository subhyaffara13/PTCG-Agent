
def test_sympy__sets__ordinals__Ordinal():
    from sympy.sets.ordinals import Ordinal, OmegaPower
    assert _test_args(Ordinal(OmegaPower(2, 1)))

