
def prim_list_unpack(
    g: jit_utils.GraphContext, *inputs, **kwargs
) -> list[_C.Value] | None:
    if len(inputs) == 1 and inputs[0].node().kind() == "prim::ListConstruct":
        # Cancel the previous node if it is ListConstruct by returning its inputs
        # TODO(justinchuby): Use a public method in the helper module
        return symbolic_helper._unpack_list(inputs[0])

    return None

