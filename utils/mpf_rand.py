
def mpf_rand(prec):
    """Return a raw mpf chosen randomly from [0, 1), with prec bits
    in the mantissa."""
    global getrandbits
    if not getrandbits:
        import random
        getrandbits = random.getrandbits
    return from_man_exp(getrandbits(prec), -prec, prec, round_floor)

