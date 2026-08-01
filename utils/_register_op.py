
def _register_op(op, func, op_table):
    """
    Performs basic validation and registers the provided op in the given
    op_table.
    """
    if len(signature(func).parameters) != 4:
        raise TypeError(
            f"Custom sharded op function expects signature: "
            f"(types, args, kwargs, process_group), but received "
            f"signature: {signature(func)}"
        )

    op_table[op] = func

