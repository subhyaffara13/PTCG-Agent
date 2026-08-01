
def __contains_(g: jit_utils.GraphContext, self, element):
    unpacked_list = symbolic_helper._unpack_list(self)
    if all(
        symbolic_helper._is_constant(x) for x in unpacked_list
    ) and symbolic_helper._is_constant(element):
        return g.op(
            "Constant",
            value_t=torch.tensor(
                symbolic_helper._node_get(element.node(), "value")
                in (symbolic_helper._node_get(x.node(), "value") for x in unpacked_list)
            ),
        )

    raise errors.SymbolicValueError(
        "Unsupported: ONNX export of __contains__ for non-constant list or element.",
        self,
    )

