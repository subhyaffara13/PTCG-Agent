
def test_C8():
    # Modular multiplicative inverse. Would be nice if divmod could do this.
    assert ZZ.invert(5, 7) == 3
    assert ZZ.invert(5, 6) == 5

