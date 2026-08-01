
def rand4x(seed, offset, n_rounds=PHILOX_N_ROUNDS_DEFAULT):
    i1, i2, i3, i4 = randint4x(seed, offset, n_rounds)
    u1 = _uint_to_uniform_float(i1)
    u2 = _uint_to_uniform_float(i2)
    u3 = _uint_to_uniform_float(i3)
    u4 = _uint_to_uniform_float(i4)
    return u1, u2, u3, u4

