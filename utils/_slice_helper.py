
def _slice_helper(
    g: jit_utils.GraphContext,
    input,
    axes,
    starts,
    ends,
    steps=None,
):
    if g.opset <= 9:
        from torch.onnx._internal.torchscript_exporter.symbolic_opset9 import (
            _slice as _slice9,
        )

        return _slice9(g, input, axes, starts, ends)
    else:
        from torch.onnx._internal.torchscript_exporter.symbolic_opset10 import (
            _slice as _slice10,
        )

        return _slice10(g, input, axes, starts, ends, steps)

