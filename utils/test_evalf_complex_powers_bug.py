
def test_evalf_complex_powers_bug():
    assert NS('(pi + pi*I)**4') == '-389.63636413601 + 0.e-14*I'

