
def test_XXM_from_flat_nz(DM):
    T = type(DM([[0]]))
    elements = [ZZ(1), ZZ(2), ZZ(3)]
    indices = ((0, 0), (0, 1), (2, 2))
    data = (indices, (3, 3))
    result = DM([[1, 2, 0], [0, 0, 0], [0, 0, 3]])
    assert T.from_flat_nz(elements, data, ZZ) == result
    raises(DMBadInputError, lambda: T.from_flat_nz(elements, (indices, (2, 3)), ZZ))

