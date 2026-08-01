
def test_dh_shared_key():
    prk = dh_private_key(digit = 100)
    p, _, ga = dh_public_key(prk)
    b = randrange(2, p)
    sk = dh_shared_key((p, _, ga), b)
    assert sk == pow(ga, b, p)
    raises(ValueError, lambda: dh_shared_key((1031, 14, 565), 2000))

