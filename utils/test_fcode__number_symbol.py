
def test_fcode_NumberSymbol():
    prec = 17
    p = FCodePrinter()
    assert fcode(Catalan) == '      parameter (Catalan = %sd0)\n      Catalan' % Catalan.evalf(prec)
    assert fcode(EulerGamma) == '      parameter (EulerGamma = %sd0)\n      EulerGamma' % EulerGamma.evalf(prec)
    assert fcode(E) == '      parameter (E = %sd0)\n      E' % E.evalf(prec)
    assert fcode(GoldenRatio) == '      parameter (GoldenRatio = %sd0)\n      GoldenRatio' % GoldenRatio.evalf(prec)
    assert fcode(pi) == '      parameter (pi = %sd0)\n      pi' % pi.evalf(prec)
    assert fcode(
        pi, precision=5) == '      parameter (pi = %sd0)\n      pi' % pi.evalf(5)
    assert fcode(Catalan, human=False) == ({
        (Catalan, p._print(Catalan.evalf(prec)))}, set(), '      Catalan')
    assert fcode(EulerGamma, human=False) == ({(EulerGamma, p._print(
        EulerGamma.evalf(prec)))}, set(), '      EulerGamma')
    assert fcode(E, human=False) == (
        {(E, p._print(E.evalf(prec)))}, set(), '      E')
    assert fcode(GoldenRatio, human=False) == ({(GoldenRatio, p._print(
        GoldenRatio.evalf(prec)))}, set(), '      GoldenRatio')
    assert fcode(pi, human=False) == (
        {(pi, p._print(pi.evalf(prec)))}, set(), '      pi')
    assert fcode(pi, precision=5, human=False) == (
        {(pi, p._print(pi.evalf(5)))}, set(), '      pi')

