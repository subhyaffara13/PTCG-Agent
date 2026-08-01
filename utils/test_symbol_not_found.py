
def test_symbol_not_found():
    e = a*a + b
    raises(LookupError, lambda: g.llvm_callable([a], e))

