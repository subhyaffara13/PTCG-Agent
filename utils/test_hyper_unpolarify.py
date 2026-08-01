
def test_hyper_unpolarify():
    from sympy.functions.elementary.exponential import exp_polar
    a = exp_polar(2*pi*I)*x
    b = x
    assert hyper([], [], a).argument == b
    assert hyper([0], [], a).argument == a
    assert hyper([0], [0], a).argument == b
    assert hyper([0, 1], [0], a).argument == a
    assert hyper([0, 1], [0], exp_polar(2*pi*I)).argument == 1

