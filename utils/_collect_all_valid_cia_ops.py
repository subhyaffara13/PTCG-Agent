
def _collect_all_valid_cia_ops() -> set["OperatorBase"]:
    """
    This is an util function that gets the all CIA functional ops.

    The algorithm is in 2 steps:
      1. We first query C++ dispatcher to get the list of CIA ops
         and then we call getattr on torch.ops.aten to lazily populate
         them.

      2. Sometimes, handful of ops have CIA registered in python dispatcher
         but not on the C++ side, these can't be caught at the first step.
         So we walk again to get the final list.

    Note that the output of this function should never be modified
    """
    cia_ops = set()
    for op_namespace_name in torch.ops._dir:
        # The reason we split here is because aten ops are safe to cache.
        if op_namespace_name != "aten":
            if not hasattr(torch.ops, op_namespace_name):
                raise AssertionError(
                    f"torch.ops does not have attribute {op_namespace_name!r}"
                )
            op_namespace = getattr(torch.ops, op_namespace_name)
            if isinstance(op_namespace, torch._ops._OpNamespace):
                cia_ops |= _collect_all_valid_cia_ops_for_namespace(op_namespace)
        else:
            cia_ops |= _collect_all_valid_cia_ops_for_aten_namespace()
    return cia_ops

