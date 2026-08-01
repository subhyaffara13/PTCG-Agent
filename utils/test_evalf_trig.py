
def test_evalf_trig():
    assert NS('sin(1)', 15) == '0.841470984807897'
    assert NS('cos(1)', 15) == '0.540302305868140'
    assert NS('tan(1)', 15) == '1.55740772465490'
    assert NS('sin(10**-6)', 15) == '9.99999999999833e-7'
    assert NS('cos(10**-6)', 15) == '0.999999999999500'
    assert NS('tan(10**-6)', 15) == '1.00000000000033e-6'
    assert NS('sin(E*10**100)', 15) == '0.409160531722613'
    assert NS('tan(I)',15) =='0.761594155955765*I'
    assert NS('tan(1000*I)',15)== '1.00000000000000*I'
    # Some input near roots
    assert NS(sin(exp(pi*sqrt(163))*pi), 15) == '-2.35596641936785e-12'
    assert NS(sin(pi*10**100 + Rational(7, 10**5), evaluate=False), 15, maxn=120) == \
        '6.99999999428333e-5'
    assert NS(sin(Rational(7, 10**5), evaluate=False), 15) == \
        '6.99999999428333e-5'

