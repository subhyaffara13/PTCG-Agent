
def test_Domain_characteristic():
    for F, c in [(FF(3), 3), (FF(5), 5), (FF(7), 7)]:
        for R in F, F[x], F.frac_field(x), F.old_poly_ring(x), F.old_frac_field(x):
            assert R.has_CharacteristicZero is False
            assert R.characteristic() == c
    for D in ZZ, QQ, ZZ_I, QQ_I, ALG:
        for R in D, D[x], D.frac_field(x), D.old_poly_ring(x), D.old_frac_field(x):
            assert R.has_CharacteristicZero is True
            assert R.characteristic() == 0

