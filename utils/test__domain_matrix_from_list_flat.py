
def test_DomainMatrix_from_list_flat():
    nums = [ZZ(1), ZZ(2), ZZ(3), ZZ(4)]
    A = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)

    assert DomainMatrix.from_list_flat(nums, (2, 2), ZZ) == A
    assert DDM.from_list_flat(nums, (2, 2), ZZ) == A.rep.to_ddm()
    assert SDM.from_list_flat(nums, (2, 2), ZZ) == A.rep.to_sdm()

    assert A == A.from_list_flat(A.to_list_flat(), A.shape, A.domain)

    raises(DMBadInputError, DomainMatrix.from_list_flat, nums, (2, 3), ZZ)
    raises(DMBadInputError, DDM.from_list_flat, nums, (2, 3), ZZ)
    raises(DMBadInputError, SDM.from_list_flat, nums, (2, 3), ZZ)

