
def test_XXM_nullspace_QQ(DM):
    dM1 = DM([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # XXX: Change the signature to just return the nullspace. Possibly
    # returning the rank or nullity makes sense but the list of nonpivots is
    # not useful.
    assert dM1.nullspace() == (DM([[1, -2, 1]]), [2])

