
def test_latex_FormalPowerSeries():
    latex_str = r'\sum_{k=1}^{\infty} - \frac{\left(-1\right)^{- k} x^{k}}{k}'
    assert latex(fps(log(1 + x))) == latex_str

