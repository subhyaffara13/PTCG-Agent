
def test_latex_productset():
    line = Interval(0, 1)
    bigline = Interval(0, 10)
    fset = FiniteSet(1, 2, 3)
    assert latex(line**2) == r"%s^{2}" % latex(line)
    assert latex(line**10) == r"%s^{10}" % latex(line)
    assert latex((line * bigline * fset).flatten()) == r"%s \times %s \times %s" % (
        latex(line), latex(bigline), latex(fset))

