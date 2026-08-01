
def test_dup_zz_factor():
    R, x = ring("x", ZZ)

    assert R.dup_zz_factor(0) == (0, [])
    assert R.dup_zz_factor(7) == (7, [])
    assert R.dup_zz_factor(-7) == (-7, [])

    assert R.dup_zz_factor_sqf(0) == (0, [])
    assert R.dup_zz_factor_sqf(7) == (7, [])
    assert R.dup_zz_factor_sqf(-7) == (-7, [])

    assert R.dup_zz_factor(2*x + 4) == (2, [(x + 2, 1)])
    assert R.dup_zz_factor_sqf(2*x + 4) == (2, [x + 2])

    f = x**4 + x + 1

    for i in range(0, 20):
        assert R.dup_zz_factor(f) == (1, [(f, 1)])

    assert R.dup_zz_factor(x**2 + 2*x + 2) == \
        (1, [(x**2 + 2*x + 2, 1)])

    assert R.dup_zz_factor(18*x**2 + 12*x + 2) == \
        (2, [(3*x + 1, 2)])

    assert R.dup_zz_factor(-9*x**2 + 1) == \
        (-1, [(3*x - 1, 1),
              (3*x + 1, 1)])

    assert R.dup_zz_factor_sqf(-9*x**2 + 1) == \
        (-1, [3*x - 1,
              3*x + 1])

    # The order of the factors will be different when the ground types are
    # flint. At the higher level dup_factor_list will sort the factors.
    c, factors = R.dup_zz_factor(x**3 - 6*x**2 + 11*x - 6)
    assert c == 1
    assert set(factors) == {(x - 3, 1), (x - 2, 1), (x - 1, 1)}

    assert R.dup_zz_factor_sqf(x**3 - 6*x**2 + 11*x - 6) == \
        (1, [x - 3,
             x - 2,
             x - 1])

    assert R.dup_zz_factor(3*x**3 + 10*x**2 + 13*x + 10) == \
        (1, [(x + 2, 1),
             (3*x**2 + 4*x + 5, 1)])

    assert R.dup_zz_factor_sqf(3*x**3 + 10*x**2 + 13*x + 10) == \
        (1, [x + 2,
             3*x**2 + 4*x + 5])

    c, factors = R.dup_zz_factor(-x**6 + x**2)
    assert c == -1
    assert set(factors) == {(x, 2), (x - 1, 1), (x + 1, 1), (x**2 + 1, 1)}

    f = 1080*x**8 + 5184*x**7 + 2099*x**6 + 744*x**5 + 2736*x**4 - 648*x**3 + 129*x**2 - 324

    assert R.dup_zz_factor(f) == \
        (1, [(5*x**4 + 24*x**3 + 9*x**2 + 12, 1),
             (216*x**4 + 31*x**2 - 27, 1)])

    f = -29802322387695312500000000000000000000*x**25 \
      + 2980232238769531250000000000000000*x**20 \
      + 1743435859680175781250000000000*x**15 \
      + 114142894744873046875000000*x**10 \
      - 210106372833251953125*x**5 \
      + 95367431640625

    c, factors = R.dup_zz_factor(f)
    assert c == -95367431640625
    assert set(factors) == {
        (5*x - 1, 1),
        (100*x**2 + 10*x - 1, 2),
        (625*x**4 + 125*x**3 + 25*x**2 + 5*x + 1, 1),
        (10000*x**4 - 3000*x**3 + 400*x**2 - 20*x + 1, 2),
        (10000*x**4 + 2000*x**3 + 400*x**2 + 30*x + 1, 2),
    }

    f = x**10 - 1

    config.setup('USE_CYCLOTOMIC_FACTOR', True)
    c0, F_0 = R.dup_zz_factor(f)

    config.setup('USE_CYCLOTOMIC_FACTOR', False)
    c1, F_1 = R.dup_zz_factor(f)

    assert c0 == c1 == 1
    assert set(F_0) == set(F_1) == {
        (x - 1, 1),
        (x + 1, 1),
        (x**4 - x**3 + x**2 - x + 1, 1),
        (x**4 + x**3 + x**2 + x + 1, 1),
    }

    config.setup('USE_CYCLOTOMIC_FACTOR')

    f = x**10 + 1

    config.setup('USE_CYCLOTOMIC_FACTOR', True)
    F_0 = R.dup_zz_factor(f)

    config.setup('USE_CYCLOTOMIC_FACTOR', False)
    F_1 = R.dup_zz_factor(f)

    assert F_0 == F_1 == \
        (1, [(x**2 + 1, 1),
             (x**8 - x**6 + x**4 - x**2 + 1, 1)])

    config.setup('USE_CYCLOTOMIC_FACTOR')

