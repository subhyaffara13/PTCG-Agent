
def test_sympy__functions__special__zeta_functions__riemann_xi():
    from sympy.functions.special.zeta_functions import riemann_xi
    assert _test_args(riemann_xi(x))

