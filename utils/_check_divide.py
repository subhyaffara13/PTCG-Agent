
def _check_divide(result, rref_ans, den_ans):
    """Check the divided result."""
    rref, pivots = result
    if isinstance(rref, (DDM, SDM, list, dict)):
        assert type(pivots) is list
        pivots = tuple(pivots)
    rref_ans = rref_ans.to_field() / den_ans
    rref = _to_DM(rref, rref_ans)
    assert rref == rref_ans
    assert _pivots(rref) == pivots

