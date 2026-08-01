
def test_Domain_unify_with_symbols():
    raises(UnificationFailed, lambda: ZZ[x, y].unify_with_symbols(ZZ, (y, z)))
    raises(UnificationFailed, lambda: ZZ.unify_with_symbols(ZZ[x, y], (y, z)))

