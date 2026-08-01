
def test_XXM_inv_ZZ(DM):
    dM1 = DM([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
    # XXX: Maybe this should return a DM over QQ instead?
    # XXX: Handle unimodular matrices?
    raises(DMDomainError, lambda: dM1.inv())

