
def test_subexpression_postprocessors():
    # The postprocessors used to work with subexpressions, but the
    # functionality was removed. See #15948.
    a = symbols("a")
    x = SymbolInMulOnce("x")
    w = SymbolRemovesOtherSymbols("w")
    assert 3*a*w**2 == 3*w**2
    assert 3*a*x**3*w**2 == 3*w**2

    x = SubclassSymbolInMulOnce("x")
    w = SubclassSymbolRemovesOtherSymbols("w")
    assert 3*a*w**2 == 3*w**2
    assert 3*a*x**3*w**2 == 3*w**2

