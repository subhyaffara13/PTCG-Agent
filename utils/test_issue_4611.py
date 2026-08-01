
def test_issue_4611():
    assert abs(pi._evalf(50) - 3.14159265358979) < 1e-10
    assert abs(E._evalf(50) - 2.71828182845905) < 1e-10
    assert abs(Catalan._evalf(50) - 0.915965594177219) < 1e-10
    assert abs(EulerGamma._evalf(50) - 0.577215664901533) < 1e-10
    assert abs(GoldenRatio._evalf(50) - 1.61803398874989) < 1e-10
    assert abs(TribonacciConstant._evalf(50) - 1.83928675521416) < 1e-10

    x = Symbol("x")
    assert (pi + x).evalf() == pi.evalf() + x
    assert (E + x).evalf() == E.evalf() + x
    assert (Catalan + x).evalf() == Catalan.evalf() + x
    assert (EulerGamma + x).evalf() == EulerGamma.evalf() + x
    assert (GoldenRatio + x).evalf() == GoldenRatio.evalf() + x
    assert (TribonacciConstant + x).evalf() == TribonacciConstant.evalf() + x

