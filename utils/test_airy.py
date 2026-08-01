
def test_airy():
    from sympy.functions.special.bessel import (airyai, airybi)

    expr1 = airyai(x)
    expr2 = airybi(x)

    prntr = SciPyPrinter()
    assert prntr.doprint(expr1) == 'scipy.special.airy(x)[0]'
    assert prntr.doprint(expr2) == 'scipy.special.airy(x)[2]'

    prntr = NumPyPrinter({'strict': False})
    assert "Not supported" in prntr.doprint(expr1)
    assert "Not supported" in prntr.doprint(expr2)

    prntr = PythonCodePrinter({'strict': False})
    assert "Not supported" in prntr.doprint(expr1)
    assert "Not supported" in prntr.doprint(expr2)


def test_airy():
    mp.dps = 15
    assert (airyai(10)*10**10).ae(1.1047532552898687)
    assert (airybi(10)/10**9).ae(0.45564115354822515)
    assert (airyai(1000)*10**9158).ae(9.306933063179556004)
    assert (airybi(1000)/10**9154).ae(5.4077118391949465477)
    assert airyai(-1000).ae(0.055971895773019918842)
    assert airybi(-1000).ae(-0.083264574117080633012)
    assert (airyai(100+100j)*10**188).ae(2.9099582462207032076 + 2.353013591706178756j)
    assert (airybi(100+100j)/10**185).ae(1.7086751714463652039 - 3.1416590020830804578j)

