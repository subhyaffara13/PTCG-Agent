
def list_ops(cls: type[Any]):
    return OrderedSet([x for x in dir(cls) if not _ignore_op_re(x)])

