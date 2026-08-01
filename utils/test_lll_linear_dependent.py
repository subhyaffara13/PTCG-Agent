
def test_lll_linear_dependent():
    linear_dependent_test_data = [
        DM([[0, -1, -2, -3],
            [1, 0, -1, -2],
            [2, 1, 0, -1],
            [3, 2, 1, 0]], ZZ),
        DM([[1, 0, 0, 1],
            [0, 1, 0, 1],
            [0, 0, 1, 1],
            [1, 2, 3, 6]], ZZ),
        DM([[3, -5, 1],
            [4, 6, 0],
            [10, -4, 2]], ZZ)
    ]
    for not_basis in linear_dependent_test_data:
        raises(DMRankError, lambda: _ddm_lll(not_basis.rep.to_ddm()))
        raises(DMRankError, lambda: ddm_lll(not_basis.rep.to_ddm()))
        raises(DMRankError, lambda: not_basis.rep.lll())
        raises(DMRankError, lambda: not_basis.rep.to_sdm().lll())
        raises(DMRankError, lambda: not_basis.lll())
        raises(DMRankError, lambda: _ddm_lll(not_basis.rep.to_ddm(), return_transform=True))
        raises(DMRankError, lambda: ddm_lll_transform(not_basis.rep.to_ddm()))
        raises(DMRankError, lambda: not_basis.rep.lll_transform())
        raises(DMRankError, lambda: not_basis.rep.to_sdm().lll_transform())
        raises(DMRankError, lambda: not_basis.lll_transform())

