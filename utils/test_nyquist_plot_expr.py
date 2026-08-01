
def test_nyquist_plot_expr():
    r1, i1, w1 = nyquist_plot_expr(tf1)
    r2, i2, w2 = nyquist_plot_expr(tf2)
    r3, i3, w3 = nyquist_plot_expr(tf3)
    r4, i4, w4 = nyquist_plot_expr(tf4)
    assert r1 == (2 - w1**2)/(0.25*w1**2 + (2 - w1**2)**2)
    assert i1 == -0.5*w1/(0.25*w1**2 + (2 - w1**2)**2)
    assert r2 == 3*w2**2/(9*w2**2 + (1 - 6*w2**2)**2)
    assert i2 == w2*(1 - 6*w2**2)/(9*w2**2 + (1 - 6*w2**2)**2)
    assert r3 == -w3**4/(w3**6 + 1)
    assert i3 == -w3/(w3**6 + 1)
    assert r4 == 0
    assert i4 == 10/w4**3

