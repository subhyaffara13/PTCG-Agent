
def test_constants():
    assert m.some_constant == 14


def test_constants():
    assert julia_code(pi) == "pi"
    assert julia_code(oo) == "Inf"
    assert julia_code(-oo) == "-Inf"
    assert julia_code(S.NegativeInfinity) == "-Inf"
    assert julia_code(S.NaN) == "NaN"
    assert julia_code(S.Exp1) == "e"
    assert julia_code(exp(1)) == "e"


def test_constants():
    assert maple_code(pi) == "Pi"
    assert maple_code(oo) == "infinity"
    assert maple_code(-oo) == "-infinity"
    assert maple_code(S.NegativeInfinity) == "-infinity"
    assert maple_code(S.NaN) == "undefined"
    assert maple_code(S.Exp1) == "exp(1)"
    assert maple_code(exp(1)) == "exp(1)"


def test_constants():
    assert mcode(S.Zero) == "0"
    assert mcode(S.One) == "1"
    assert mcode(S.NegativeOne) == "-1"
    assert mcode(S.Half) == "1/2"
    assert mcode(S.ImaginaryUnit) == "I"

    assert mcode(oo) == "Infinity"
    assert mcode(S.NegativeInfinity) == "-Infinity"
    assert mcode(S.ComplexInfinity) == "ComplexInfinity"
    assert mcode(S.NaN) == "Indeterminate"

    assert mcode(S.Exp1) == "E"
    assert mcode(pi) == "Pi"
    assert mcode(S.GoldenRatio) == "GoldenRatio"
    assert mcode(S.TribonacciConstant) == \
        "(1/3 + (1/3)*(19 - 3*33^(1/2))^(1/3) + " \
        "(1/3)*(3*33^(1/2) + 19)^(1/3))"
    assert mcode(2*S.TribonacciConstant) == \
        "2*(1/3 + (1/3)*(19 - 3*33^(1/2))^(1/3) + " \
        "(1/3)*(3*33^(1/2) + 19)^(1/3))"
    assert mcode(S.EulerGamma) == "EulerGamma"
    assert mcode(S.Catalan) == "Catalan"


def test_constants():
    assert mcode(pi) == "pi"
    assert mcode(oo) == "inf"
    assert mcode(-oo) == "-inf"
    assert mcode(S.NegativeInfinity) == "-inf"
    assert mcode(S.NaN) == "NaN"
    assert mcode(S.Exp1) == "exp(1)"
    assert mcode(exp(1)) == "exp(1)"


def test_constants():
    assert rust_code(pi) == "PI"
    assert rust_code(oo) == "INFINITY"
    assert rust_code(S.Infinity) == "INFINITY"
    assert rust_code(-oo) == "NEG_INFINITY"
    assert rust_code(S.NegativeInfinity) == "NEG_INFINITY"
    assert rust_code(S.NaN) == "NAN"
    assert rust_code(exp(1)) == "E"
    assert rust_code(S.Exp1) == "E"


def test_constants():
    assert str(hbar) == 'hbar'
    assert pretty(hbar) == 'hbar'
    assert upretty(hbar) == 'ℏ'
    assert latex(hbar) == r'\hbar'
    sT(hbar, "HBar()")


def test_constants():
    for prec in [3, 7, 10, 15, 20, 37, 80, 100, 29]:
        mp.dps = prec
        assert pi == mpf(tpi)
        assert e == mpf(te)
        assert degree == mpf(tdegree)
        assert euler == mpf(teuler)
        assert ln2 == mpf(tln2)
        assert ln10 == mpf(tln10)
        assert catalan == mpf(tcatalan)
        assert khinchin == mpf(tkhinchin)
        assert glaisher == mpf(tglaisher)
        assert phi == mpf(tphi)
        if prec < 50:
            assert mertens == mpf(tmertens)
            assert twinprime == mpf(ttwinprime)
    mp.dps = 15
    assert pi >= -1
    assert pi > 2
    assert pi > 3
    assert pi < 4

