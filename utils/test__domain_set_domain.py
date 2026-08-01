
def test_Domain_set_domain():
    doms = [GF(5), ZZ, QQ, ALG, RR, CC, EX, ZZ[z], QQ[z], RR[z], CC[z], EX[z]]
    for D1 in doms:
        for D2 in doms:
            assert D1[x].set_domain(D2) == D2[x]
            assert D1[x, y].set_domain(D2) == D2[x, y]
            assert D1.frac_field(x).set_domain(D2) == D2.frac_field(x)
            assert D1.frac_field(x, y).set_domain(D2) == D2.frac_field(x, y)
            assert D1.old_poly_ring(x).set_domain(D2) == D2.old_poly_ring(x)
            assert D1.old_poly_ring(x, y).set_domain(D2) == D2.old_poly_ring(x, y)
            assert D1.old_frac_field(x).set_domain(D2) == D2.old_frac_field(x)
            assert D1.old_frac_field(x, y).set_domain(D2) == D2.old_frac_field(x, y)

