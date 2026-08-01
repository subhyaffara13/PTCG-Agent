
def test_perturb():
    a = fone
    b = from_float(0.99999999999999989)
    c = from_float(1.0000000000000002)
    assert mpf_perturb(a, 0, 53, round_nearest) == a
    assert mpf_perturb(a, 1, 53, round_nearest) == a
    assert mpf_perturb(a, 0, 53, round_up) == c
    assert mpf_perturb(a, 0, 53, round_ceiling) == c
    assert mpf_perturb(a, 0, 53, round_down) == a
    assert mpf_perturb(a, 0, 53, round_floor) == a
    assert mpf_perturb(a, 1, 53, round_up) == a
    assert mpf_perturb(a, 1, 53, round_ceiling) == a
    assert mpf_perturb(a, 1, 53, round_down) == b
    assert mpf_perturb(a, 1, 53, round_floor) == b
    a = mpf_neg(a)
    b = mpf_neg(b)
    c = mpf_neg(c)
    assert mpf_perturb(a, 0, 53, round_nearest) == a
    assert mpf_perturb(a, 1, 53, round_nearest) == a
    assert mpf_perturb(a, 0, 53, round_up) == a
    assert mpf_perturb(a, 0, 53, round_floor) == a
    assert mpf_perturb(a, 0, 53, round_down) == b
    assert mpf_perturb(a, 0, 53, round_ceiling) == b
    assert mpf_perturb(a, 1, 53, round_up) == c
    assert mpf_perturb(a, 1, 53, round_floor) == c
    assert mpf_perturb(a, 1, 53, round_down) == a
    assert mpf_perturb(a, 1, 53, round_ceiling) == a

