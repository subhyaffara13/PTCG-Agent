
def test_pickling_polys_polyclasses():
    from sympy.polys.polyclasses import DMP, DMF, ANP

    for c in (DMP, DMP([[ZZ(1)], [ZZ(2)], [ZZ(3)]], ZZ)):
        check(c, deprecated=['rep'])
    for c in (DMF, DMF(([ZZ(1), ZZ(2)], [ZZ(1), ZZ(3)]), ZZ)):
        check(c)
    for c in (ANP, ANP([QQ(1), QQ(2)], [QQ(1), QQ(2), QQ(3)], QQ)):
        check(c)

