
def _unique2(g: jit_utils.GraphContext, self, sorted, return_inverse, return_counts):
    u, _indices, inverse_indices, counts = g.op(
        "Unique", self, sorted_i=sorted, outputs=4
    )
    return u, inverse_indices, counts


def _unique2(
    g: jit_utils.GraphContext, input, sorted, return_inverse, return_counts
) -> None:
    symbolic_helper._onnx_opset_unsupported("_unique2", 9, 11, input)

