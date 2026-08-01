
def test_Add_is_imaginary():
    nn = Dummy(nonnegative=True)
    assert (I*nn + I).is_imaginary  # issue 8046, 17

