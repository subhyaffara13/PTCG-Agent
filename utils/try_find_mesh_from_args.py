
def try_find_mesh_from_args(
    op_call: torch._ops.OpOverload, args: Sequence[object]
) -> DeviceMesh:
    """
    Find the device mesh object from args.
    It returns None if no mesh is found.
    NOTE: we can optimize this search if needed
    """
    for arg in args:
        if isinstance(arg, (dtensor.DTensor, DTensorSpec)):
            return arg.device_mesh
        elif (
            isinstance(arg, (list, tuple))
            and len(arg) > 0
            and isinstance(arg[0], (dtensor.DTensor, DTensorSpec))
        ):
            return arg[0].device_mesh

    raise ValueError(f"Cannot find device mesh from args for op : {op_call}.")

