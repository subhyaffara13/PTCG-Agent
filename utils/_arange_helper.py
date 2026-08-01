
def _arange_helper(g: jit_utils.GraphContext, *args):
    if g.opset <= 10:
        from torch.onnx._internal.torchscript_exporter.symbolic_opset9 import arange
    else:
        from torch.onnx._internal.torchscript_exporter.symbolic_opset11 import (
            arange,  # type: ignore[no-redef]
        )
    return arange(g, *args)

