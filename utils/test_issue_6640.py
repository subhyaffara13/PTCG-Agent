
def test_issue_6640():
    from mpmath.libmp.libmpf import finf, fninf
    # fnan is not included because Float no longer returns fnan,
    # but otherwise, the same sort of test could apply
    assert Float(finf).is_zero is False
    assert Float(fninf).is_zero is False
    assert bool(Float(0)) is False

