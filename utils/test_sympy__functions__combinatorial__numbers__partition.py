
def test_sympy__functions__combinatorial__numbers__partition():
    from sympy.core.symbol import Symbol
    from sympy.functions.combinatorial.numbers import partition
    assert _test_args(partition(Symbol('a', integer=True)))

