
def _sharded_op_impl(func):
    """
    Decorator to register a default sharded op.
    """
    return functools.partial(_decorator_func, op=func, op_table=_SHARDED_OPS)

