
def test_realgaunt():
    # All non-zero values corresponding to l values from 0 to 2
    for l in range(3):
        for m in range(-l, l+1):
            assert real_gaunt(0, l, l, 0, m, m) == 1/(2*sqrt(pi))
    assert real_gaunt(1, 1, 2, 0, 0, 0) == sqrt(5)/(5*sqrt(pi))
    assert real_gaunt(1, 1, 2, 1, 1, 0) == -sqrt(5)/(10*sqrt(pi))
    assert real_gaunt(2, 2, 2, 0, 0, 0) == sqrt(5)/(7*sqrt(pi))
    assert real_gaunt(2, 2, 2, 0, 2, 2) == -sqrt(5)/(7*sqrt(pi))
    assert real_gaunt(2, 2, 2, -2, -2, 0) == -sqrt(5)/(7*sqrt(pi))
    assert real_gaunt(1, 1, 2, -1, 0, -1) == sqrt(15)/(10*sqrt(pi))
    assert real_gaunt(1, 1, 2, 0, 1, 1) == sqrt(15)/(10*sqrt(pi))
    assert real_gaunt(1, 1, 2, 1, 1, 2) == sqrt(15)/(10*sqrt(pi))
    assert real_gaunt(1, 1, 2, -1, 1, -2) == sqrt(15)/(10*sqrt(pi))
    assert real_gaunt(1, 1, 2, -1, -1, 2) == -sqrt(15)/(10*sqrt(pi))
    assert real_gaunt(2, 2, 2, 0, 1, 1) == sqrt(5)/(14*sqrt(pi))
    assert real_gaunt(2, 2, 2, 1, 1, 2) == sqrt(15)/(14*sqrt(pi))
    assert real_gaunt(2, 2, 2, -1, -1, 2) == -sqrt(15)/(14*sqrt(pi))

    assert real_gaunt(-2, -2, -2, -2, -2, 0) is S.Zero  # m test
    assert real_gaunt(-2, 1, 0, 1, 1, 1) is S.Zero  # l test
    assert real_gaunt(-2, -1, -2, -1, -1, 0) is S.Zero  # m and l test
    assert real_gaunt(-2, -2, -2, -2, -2, -2) is S.Zero  # m and k test
    assert real_gaunt(-2, -1, -2, -1, -1, -1) is S.Zero  # m, l and k test

    x = symbols('x', integer=True)
    v = [0]*6
    for i in range(len(v)):
        v[i] = x  # non literal ints fail
        raises(ValueError, lambda: real_gaunt(*v))
        v[i] = 0

