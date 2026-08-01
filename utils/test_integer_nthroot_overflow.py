
def test_integer_nthroot_overflow():
    assert integer_nthroot(10**(50*50), 50) == (10**50, True)
    assert integer_nthroot(10**100000, 10000) == (10**10, True)

