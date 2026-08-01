
def test_Domain_is_Exact():
    exact = [GF(5), ZZ, QQ, ALG, EX]
    inexact = [RR, CC]
    for D in exact + inexact:
        for R in D, D[x], D.frac_field(x), D.old_poly_ring(x), D.old_frac_field(x):
            if D in exact:
                assert R.is_Exact is True
            else:
                assert R.is_Exact is False

