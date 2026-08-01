
def test_zero_assumptions():
    nr = Symbol('nonreal', real=False, finite=True)
    ni = Symbol('nonimaginary', imaginary=False)
    # imaginary implies not zero
    nzni = Symbol('nonzerononimaginary', zero=False, imaginary=False)

    assert re(nr).is_zero is None
    assert im(nr).is_zero is False

    assert re(ni).is_zero is None
    assert im(ni).is_zero is None

    assert re(nzni).is_zero is False
    assert im(nzni).is_zero is None

