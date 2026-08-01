
def _index_fill_reshape_helper(g: jit_utils.GraphContext, self, dim, index):
    # 1. reshape index => [1, ..., 1, dim, 1, ..., 1]
    # 2. expand index => [..., dim, ...], same shape as self except for dim.
    # 3. expand value as well.
    # 4. apply onnx::scatter.

    from torch.onnx._internal.torchscript_exporter.symbolic_opset9 import expand

    if g.opset <= 10:
        from torch.onnx._internal.torchscript_exporter.symbolic_opset9 import scatter
    else:
        # for mypy, scatter was imported two lines above
        from torch.onnx._internal.torchscript_exporter.symbolic_opset11 import (
            scatter,  # type: ignore[no-redef]
        )

    if self.type().dim() is None:
        return _unimplemented("index_fill", "input rank not accessible")
    self_dim = self.type().dim()
    dim_value = _parse_arg(dim, "i")
    if dim_value < 0:
        dim_value += self_dim
    unsqueezed_index = _unsqueeze_helper(
        g, index, [i for i in range(self_dim) if i != dim_value]
    )
    expanded_index_shape = scatter(
        g, g.op("Shape", self), 0, _unsqueeze_helper(g, dim, [0]), g.op("Shape", index)
    )
    expanded_index = expand(g, unsqueezed_index, expanded_index_shape, None)
    return expanded_index_shape, expanded_index

