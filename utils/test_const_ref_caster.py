
def test_const_ref_caster():
    """Verifies that const-ref is propagated through type_caster cast_op.
    The returned ConstRefCasted type is a minimal type that is constructed to
    reference the casting mode used.
    """
    x = False
    assert m.takes(x) == 1
    assert m.takes_move(x) == 1

    assert m.takes_ptr(x) == 3
    assert m.takes_ref(x) == 2
    assert m.takes_ref_wrap(x) == 2

    assert m.takes_const_ptr(x) == 5
    assert m.takes_const_ref(x) == 4
    assert m.takes_const_ref_wrap(x) == 4

