
def test_hex_pi_nth_digits():
    assert pi_hex_digits(0) == '3243f6a8885a30'
    assert pi_hex_digits(1) ==  '243f6a8885a308'
    assert pi_hex_digits(10000) == '68ac8fcfb8016c'
    assert pi_hex_digits(13) == '08d313198a2e03'
    assert pi_hex_digits(0, 3) == '324'
    assert pi_hex_digits(0, 0) == ''
    raises(ValueError, lambda: pi_hex_digits(-1))
    raises(ValueError, lambda: pi_hex_digits(0, -1))
    raises(ValueError, lambda: pi_hex_digits(3.14))

    # this will pick a random segment to compute every time
    # it is run. If it ever fails, there is an error in the
    # computation.
    n = randint(0, len(dig))
    prec = randint(0, len(dig) - n)
    assert pi_hex_digits(n, prec) == dig[n: n + prec]

