
def _text_x_broken():
    # represent has some broken logic that is relying in particular
    # forms of input, rather than a full and proper handling of
    # all valid quantum expressions. Marking this test as XFAIL until
    # we can refactor represent.
    assert represent(XOp()*XKet()*XBra('y')) == \
        x*DiracDelta(x - x_3)*DiracDelta(x_1 - y)

