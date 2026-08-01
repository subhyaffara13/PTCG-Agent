
def _check_primitive(null, null_ans):
    """Check that the primitive of the answer matches."""
    null = _to_DM(null, null_ans)
    cont, null_prim = null.primitive()
    assert null_prim == null_ans

