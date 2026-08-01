
def test_Domain_convert():

    def check_element(e1, e2, K1, K2, K3):
        if isinstance(e1, PolyElement):
            assert isinstance(e2, PolyElement) and e1.ring == e2.ring
        elif isinstance(e1, FracElement):
            assert isinstance(e2, FracElement) and e1.field == e2.field
        else:
            assert type(e1) is type(e2), '%s, %s: %s %s -> %s' % (e1, e2, K1, K2, K3)
        assert e1 == e2, '%s, %s: %s %s -> %s' % (e1, e2, K1, K2, K3)

    def check_domains(K1, K2):
        K3 = K1.unify(K2)
        check_element(K3.convert_from(K1.one, K1),  K3.one,  K1, K2, K3)
        check_element(K3.convert_from(K2.one, K2),  K3.one,  K1, K2, K3)
        check_element(K3.convert_from(K1.zero, K1), K3.zero, K1, K2, K3)
        check_element(K3.convert_from(K2.zero, K2), K3.zero, K1, K2, K3)

    def composite_domains(K):
        domains = [
            K,
            K[y], K[z], K[y, z],
            K.frac_field(y), K.frac_field(z), K.frac_field(y, z),
            # XXX: These should be tested and made to work...
            # K.old_poly_ring(y), K.old_frac_field(y),
        ]
        return domains

    QQ2 = QQ.algebraic_field(sqrt(2))
    QQ3 = QQ.algebraic_field(sqrt(3))
    doms = [ZZ, QQ, QQ2, QQ3, QQ_I, ZZ_I, RR, CC]

    for i, K1 in enumerate(doms):
        for K2 in doms[i:]:
            for K3 in composite_domains(K1):
                for K4 in composite_domains(K2):
                    check_domains(K3, K4)

    assert QQ.convert(10e-52) == QQ(1684996666696915, 1684996666696914987166688442938726917102321526408785780068975640576)

    R, xr = ring("x", ZZ)
    assert ZZ.convert(xr - xr) == 0
    assert ZZ.convert(xr - xr, R.to_domain()) == 0

    assert CC.convert(ZZ_I(1, 2)) == CC(1, 2)
    assert CC.convert(QQ_I(1, 2)) == CC(1, 2)

    assert QQ.convert_from(RR(0.5), RR) == QQ(1, 2)
    assert RR.convert_from(QQ(1, 2), QQ) == RR(0.5)
    assert QQ_I.convert_from(CC(0.5, 0.75), CC) == QQ_I(QQ(1, 2), QQ(3, 4))
    assert CC.convert_from(QQ_I(QQ(1, 2), QQ(3, 4)), QQ_I) == CC(0.5, 0.75)

    K1 = QQ.frac_field(x)
    K2 = ZZ.frac_field(x)
    K3 = QQ[x]
    K4 = ZZ[x]
    Ks = [K1, K2, K3, K4]
    for Ka, Kb in product(Ks, Ks):
        assert Ka.convert_from(Kb.from_sympy(x), Kb) == Ka.from_sympy(x)

    assert K2.convert_from(QQ(1, 2), QQ) == K2(QQ(1, 2))

