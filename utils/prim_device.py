
def prim_device(g: jit_utils.GraphContext, *inputs, **kwargs) -> None:
    output_type = g.original_node.output().type()
    if isinstance(output_type, _C.DeviceObjType):
        return None

    return symbolic_helper._unimplemented(
        "prim::device",
        f"output type should be 'DeviceObjType', not '{output_type.kind()}'",
        g.original_node.output(),
    )

