
def test_symbol_infinitereal_mul():
    ix = Symbol('ix', infinite=True, extended_real=True)
    assert (-ix).is_extended_positive is None

