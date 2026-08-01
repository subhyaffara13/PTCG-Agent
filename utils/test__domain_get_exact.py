
def test_Domain_get_exact():
    assert EX.get_exact() == EX
    assert ZZ.get_exact() == ZZ
    assert QQ.get_exact() == QQ
    assert RR.get_exact() == QQ
    assert CC.get_exact() == QQ_I
    assert ALG.get_exact() == ALG
    assert ZZ[x].get_exact() == ZZ[x]
    assert QQ[x].get_exact() == QQ[x]
    assert RR[x].get_exact() == QQ[x]
    assert CC[x].get_exact() == QQ_I[x]
    assert ZZ[x, y].get_exact() == ZZ[x, y]
    assert QQ[x, y].get_exact() == QQ[x, y]
    assert RR[x, y].get_exact() == QQ[x, y]
    assert CC[x, y].get_exact() == QQ_I[x, y]
    assert ZZ.frac_field(x).get_exact() == ZZ.frac_field(x)
    assert QQ.frac_field(x).get_exact() == QQ.frac_field(x)
    assert RR.frac_field(x).get_exact() == QQ.frac_field(x)
    assert CC.frac_field(x).get_exact() == QQ_I.frac_field(x)
    assert ZZ.frac_field(x, y).get_exact() == ZZ.frac_field(x, y)
    assert QQ.frac_field(x, y).get_exact() == QQ.frac_field(x, y)
    assert RR.frac_field(x, y).get_exact() == QQ.frac_field(x, y)
    assert CC.frac_field(x, y).get_exact() == QQ_I.frac_field(x, y)
    assert ZZ.old_poly_ring(x).get_exact() == ZZ.old_poly_ring(x)
    assert QQ.old_poly_ring(x).get_exact() == QQ.old_poly_ring(x)
    assert RR.old_poly_ring(x).get_exact() == QQ.old_poly_ring(x)
    assert CC.old_poly_ring(x).get_exact() == QQ_I.old_poly_ring(x)
    assert ZZ.old_poly_ring(x, y).get_exact() == ZZ.old_poly_ring(x, y)
    assert QQ.old_poly_ring(x, y).get_exact() == QQ.old_poly_ring(x, y)
    assert RR.old_poly_ring(x, y).get_exact() == QQ.old_poly_ring(x, y)
    assert CC.old_poly_ring(x, y).get_exact() == QQ_I.old_poly_ring(x, y)
    assert ZZ.old_frac_field(x).get_exact() == ZZ.old_frac_field(x)
    assert QQ.old_frac_field(x).get_exact() == QQ.old_frac_field(x)
    assert RR.old_frac_field(x).get_exact() == QQ.old_frac_field(x)
    assert CC.old_frac_field(x).get_exact() == QQ_I.old_frac_field(x)
    assert ZZ.old_frac_field(x, y).get_exact() == ZZ.old_frac_field(x, y)
    assert QQ.old_frac_field(x, y).get_exact() == QQ.old_frac_field(x, y)
    assert RR.old_frac_field(x, y).get_exact() == QQ.old_frac_field(x, y)
    assert CC.old_frac_field(x, y).get_exact() == QQ_I.old_frac_field(x, y)

