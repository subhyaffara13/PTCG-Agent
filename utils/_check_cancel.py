
def _check_cancel(result, rref_ans, den_ans):
    """Check the cancelled result."""
    rref, den, pivots = result
    if isinstance(rref, (DDM, SDM, list, dict)):
        assert type(pivots) is list
        pivots = tuple(pivots)
    rref = _to_DM(rref, rref_ans)
    rref2, den2 = rref.cancel_denom(den)
    assert rref2 == rref_ans
    assert den2 == den_ans
    assert pivots == _pivots(rref)

