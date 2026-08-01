
def test_sympy__functions__elementary__complexes__periodic_argument():
    from sympy.functions.elementary.complexes import periodic_argument
    assert _test_args(periodic_argument(x, y))

