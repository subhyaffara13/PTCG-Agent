
def test_EX_convert():

    elements = [
        (ZZ, ZZ(3)),
        (QQ, QQ(1,2)),
        (ZZ_I, ZZ_I(1,2)),
        (QQ_I, QQ_I(1,2)),
        (RR, RR(3)),
        (CC, CC(1,2)),
        (EX, EX(3)),
        (EXRAW, EXRAW(3)),
        (ALG, ALG.from_sympy(sqrt(2))),
    ]

    for R, e in elements:
        for EE in EX, EXRAW:
            elem = EE.from_sympy(R.to_sympy(e))
            assert EE.convert_from(e, R) == elem
            assert R.convert_from(elem, EE) == e

