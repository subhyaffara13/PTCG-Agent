
def _check_divided(null, null_ans):
    """Check the divided answer."""
    null = _to_DM(null, null_ans)
    null_ans_norm = _divide_last(null_ans)
    assert null == null_ans_norm

