
def test_Add_as_coeff_mul():
    # issue 5524.  These should all be (1, self)
    assert (x + 1).as_coeff_mul() == (1, (x + 1,))
    assert (x + 2).as_coeff_mul() == (1, (x + 2,))
    assert (x + 3).as_coeff_mul() == (1, (x + 3,))

    assert (x - 1).as_coeff_mul() == (1, (x - 1,))
    assert (x - 2).as_coeff_mul() == (1, (x - 2,))
    assert (x - 3).as_coeff_mul() == (1, (x - 3,))

    n = Symbol('n', integer=True)
    assert (n + 1).as_coeff_mul() == (1, (n + 1,))
    assert (n + 2).as_coeff_mul() == (1, (n + 2,))
    assert (n + 3).as_coeff_mul() == (1, (n + 3,))

    assert (n - 1).as_coeff_mul() == (1, (n - 1,))
    assert (n - 2).as_coeff_mul() == (1, (n - 2,))
    assert (n - 3).as_coeff_mul() == (1, (n - 3,))

