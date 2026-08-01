
def test_core_float_copy():
    # See gh-7457
    y = Symbol("x") + 1.0
    check(y)  # does not raise TypeError ("argument is not an mpz")

