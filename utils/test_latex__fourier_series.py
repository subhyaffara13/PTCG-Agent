
def test_latex_FourierSeries():
    latex_str = \
        r'2 \sin{\left(x \right)} - \sin{\left(2 x \right)} + \frac{2 \sin{\left(3 x \right)}}{3} + \ldots'
    assert latex(fourier_series(x, (x, -pi, pi))) == latex_str

