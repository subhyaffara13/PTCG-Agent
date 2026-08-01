
def test_trig_misc_hard():
    mp.prec = 53
    # Worst-case input for an IEEE double, from a paper by Kahan
    x = ldexp(6381956970095103,797)
    assert cos(x) == mpf('-4.6871659242546277e-19')
    assert sin(x) == 1

    mp.prec = 150
    a = mpf(10**50)
    mp.prec = 53
    assert sin(a).ae(-0.7896724934293100827)
    assert cos(a).ae(-0.6135286082336635622)

    # Check relative accuracy close to x = zero
    assert sin(1e-100) == 1e-100  # when rounding to nearest
    assert sin(1e-6).ae(9.999999999998333e-007, rel_eps=2e-15, abs_eps=0)
    assert sin(1e-6j).ae(1.0000000000001666e-006j, rel_eps=2e-15, abs_eps=0)
    assert sin(-1e-6j).ae(-1.0000000000001666e-006j, rel_eps=2e-15, abs_eps=0)
    assert cos(1e-100) == 1
    assert cos(1e-6).ae(0.9999999999995)
    assert cos(-1e-6j).ae(1.0000000000005)
    assert tan(1e-100) == 1e-100
    assert tan(1e-6).ae(1.0000000000003335e-006, rel_eps=2e-15, abs_eps=0)
    assert tan(1e-6j).ae(9.9999999999966644e-007j, rel_eps=2e-15, abs_eps=0)
    assert tan(-1e-6j).ae(-9.9999999999966644e-007j, rel_eps=2e-15, abs_eps=0)

