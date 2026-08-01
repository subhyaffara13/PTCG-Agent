
def _special_op_to_preserve_cia(*args, **kwargs):
    """
    This is an special marker that tells our infra that we shouldn't decompose this op.
    """
    return NotImplemented

