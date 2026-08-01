
def test_nichols_expr():
    m1, p1, w1 = nichols_plot_expr(tf1)
    m2, p2, w2 = nichols_plot_expr(tf2)
    m3, p3, w3 = nichols_plot_expr(tf3)
    m4, p4, w4 = nichols_plot_expr(tf4)
    assert m1 == 20*log(1/sqrt(w1**4 - 3.75*w1**2 + 4))/log(10)
    assert p1 == 180*arg(1/(-w1**2 + 0.5*w1*I + 2))/pi
    assert m2 == 20*log(Abs(w2)/sqrt(36*w2**4 - 3*w2**2 + 1))/log(10)
    assert p2 == 180*arg(w2*I/(-6*w2**2 + 3*w2*I + 1))/pi
    assert m3 == 20*log(Abs(w3)/sqrt(w3**6 + 1))/log(10)
    assert p3 == 180*arg(-w3*I/(w3**3*I + 1))/pi
    assert m4 == 20*log(10/(w4**2*Abs(w4)))/log(10)
    assert p4 == 180*arg(I/w4**3)/pi

