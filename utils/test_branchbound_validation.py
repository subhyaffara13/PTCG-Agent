
def test_branchbound_validation() -> None:
    with pytest.raises(ValueError):
        oe.BranchBound(nbranch=0)

