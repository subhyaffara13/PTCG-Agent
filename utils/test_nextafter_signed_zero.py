
def test_nextafter_signed_zero(sctype):
    """`nextafter(-0.0, +0.0)` must return the sign of the second parameter"""

    def _equal_signed_zero(a, b):
        return (a == b) and (np.signbit(a) == np.signbit(b))

    pos_zero = sctype(+0.0)
    neg_zero = sctype(-0.0)

    assert _equal_signed_zero(np.nextafter(pos_zero, neg_zero), neg_zero), \
        f"nextafter(+0.0, -0.0) != -0.0 for {sctype.__name__}"
    assert _equal_signed_zero(np.nextafter(neg_zero, pos_zero), pos_zero), \
        f"nextafter(-0.0, +0.0) != +0.0 for {sctype.__name__}"

    assert _equal_signed_zero(np.nextafter(pos_zero, pos_zero), pos_zero), \
        f"nextafter(+0.0, +0.0) != +0.0 for {sctype.__name__}"
    assert _equal_signed_zero(np.nextafter(neg_zero, neg_zero), neg_zero), \
        f"nextafter(-0.0, -0.0) != -0.0 for {sctype.__name__}"

