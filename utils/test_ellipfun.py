
def test_ellipfun():
    mp.dps = 15
    assert ellipfun('ss', 0, 0) == 1
    assert ellipfun('cc', 0, 0) == 1
    assert ellipfun('dd', 0, 0) == 1
    assert ellipfun('nn', 0, 0) == 1
    assert ellipfun('sn', 0.25, 0).ae(sin(0.25))
    assert ellipfun('cn', 0.25, 0).ae(cos(0.25))
    assert ellipfun('dn', 0.25, 0).ae(1)
    assert ellipfun('ns', 0.25, 0).ae(csc(0.25))
    assert ellipfun('nc', 0.25, 0).ae(sec(0.25))
    assert ellipfun('nd', 0.25, 0).ae(1)
    assert ellipfun('sc', 0.25, 0).ae(tan(0.25))
    assert ellipfun('sd', 0.25, 0).ae(sin(0.25))
    assert ellipfun('cd', 0.25, 0).ae(cos(0.25))
    assert ellipfun('cs', 0.25, 0).ae(cot(0.25))
    assert ellipfun('dc', 0.25, 0).ae(sec(0.25))
    assert ellipfun('ds', 0.25, 0).ae(csc(0.25))
    assert ellipfun('sn', 0.25, 1).ae(tanh(0.25))
    assert ellipfun('cn', 0.25, 1).ae(sech(0.25))
    assert ellipfun('dn', 0.25, 1).ae(sech(0.25))
    assert ellipfun('ns', 0.25, 1).ae(coth(0.25))
    assert ellipfun('nc', 0.25, 1).ae(cosh(0.25))
    assert ellipfun('nd', 0.25, 1).ae(cosh(0.25))
    assert ellipfun('sc', 0.25, 1).ae(sinh(0.25))
    assert ellipfun('sd', 0.25, 1).ae(sinh(0.25))
    assert ellipfun('cd', 0.25, 1).ae(1)
    assert ellipfun('cs', 0.25, 1).ae(csch(0.25))
    assert ellipfun('dc', 0.25, 1).ae(1)
    assert ellipfun('ds', 0.25, 1).ae(csch(0.25))
    assert ellipfun('sn', 0.25, 0.5).ae(0.24615967096986145833)
    assert ellipfun('cn', 0.25, 0.5).ae(0.96922928989378439337)
    assert ellipfun('dn', 0.25, 0.5).ae(0.98473484156599474563)
    assert ellipfun('ns', 0.25, 0.5).ae(4.0624038700573130369)
    assert ellipfun('nc', 0.25, 0.5).ae(1.0317476065024692949)
    assert ellipfun('nd', 0.25, 0.5).ae(1.0155017958029488665)
    assert ellipfun('sc', 0.25, 0.5).ae(0.25397465134058993408)
    assert ellipfun('sd', 0.25, 0.5).ae(0.24997558792415733063)
    assert ellipfun('cd', 0.25, 0.5).ae(0.98425408443195497052)
    assert ellipfun('cs', 0.25, 0.5).ae(3.9374008182374110826)
    assert ellipfun('dc', 0.25, 0.5).ae(1.0159978158253033913)
    assert ellipfun('ds', 0.25, 0.5).ae(4.0003906313579720593)

