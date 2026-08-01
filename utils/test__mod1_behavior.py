
def test_Mod1_behavior():
    from sympy.core.symbol import Symbol
    from sympy.simplify.simplify import simplify
    n = Symbol('n', integer=True)
    # Note: this should not hang.
    assert simplify(hyperexpand(meijerg([1], [], [n + 1], [0], z))) == \
        lowergamma(n + 1, z)

