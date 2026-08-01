
def test_gf_ddf():
    f = gf_from_dict({15: ZZ(1), 0: ZZ(-1)}, 11, ZZ)
    g = [([1, 0, 0, 0, 0, 10], 1),
         ([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], 2)]

    assert gf_ddf_zassenhaus(f, 11, ZZ) == g
    assert gf_ddf_shoup(f, 11, ZZ) == g

    f = gf_from_dict({63: ZZ(1), 0: ZZ(1)}, 2, ZZ)
    g = [([1, 1], 1),
         ([1, 1, 1], 2),
         ([1, 1, 1, 1, 1, 1, 1], 3),
         ([1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0,
           0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0,
           0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1], 6)]

    assert gf_ddf_zassenhaus(f, 2, ZZ) == g
    assert gf_ddf_shoup(f, 2, ZZ) == g

    f = gf_from_dict({6: ZZ(1), 5: ZZ(-1), 4: ZZ(1), 3: ZZ(1), 1: ZZ(-1)}, 3, ZZ)
    g = [([1, 1, 0], 1),
         ([1, 1, 0, 1, 2], 2)]

    assert gf_ddf_zassenhaus(f, 3, ZZ) == g
    assert gf_ddf_shoup(f, 3, ZZ) == g

    f = ZZ.map([1, 2, 5, 26, 677, 436, 791, 325, 456, 24, 577])
    g = [([1, 701], 1),
         ([1, 110, 559, 532, 694, 151, 110, 70, 735, 122], 9)]

    assert gf_ddf_zassenhaus(f, 809, ZZ) == g
    assert gf_ddf_shoup(f, 809, ZZ) == g

    p = ZZ(nextprime(int((2**15 * pi).evalf())))
    f = gf_from_dict({15: 1, 1: 1, 0: 1}, p, ZZ)
    g = [([1, 22730, 68144], 2),
         ([1, 64876, 83977, 10787, 12561, 68608, 52650, 88001, 84356], 4),
         ([1, 15347, 95022, 84569, 94508, 92335], 5)]

    assert gf_ddf_zassenhaus(f, p, ZZ) == g
    assert gf_ddf_shoup(f, p, ZZ) == g

