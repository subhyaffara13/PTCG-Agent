
def test_IndexedBase_assumptions_inheritance():
    I = Symbol('I', integer=True)
    I_inherit = IndexedBase(I)
    I_explicit = IndexedBase('I', integer=True)

    assert I_inherit.is_integer
    assert I_explicit.is_integer
    assert I_inherit.label.is_integer
    assert I_explicit.label.is_integer
    assert I_inherit == I_explicit

