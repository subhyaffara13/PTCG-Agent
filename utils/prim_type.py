
def prim_type(g: jit_utils.GraphContext, device_value: _C.Value, *args, **kwargs):
    if device_value.node().kind() == "prim::device":
        device = jit_utils.get_device_from_value(device_value.node().input())
        if device is not None:
            return g.op("Constant", value_s=str(device))

    return symbolic_helper._unimplemented(
        "prim::type",
        "Device type cannot be statically determined.",
        device_value,
    )

