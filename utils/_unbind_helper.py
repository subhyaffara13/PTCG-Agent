
def _unbind_helper(g: jit_utils.GraphContext, self, dim, _outputs):
    if g.opset < 11:
        from torch.onnx._internal.torchscript_exporter.symbolic_opset9 import unbind
    elif g.opset <= 12:
        from torch.onnx._internal.torchscript_exporter.symbolic_opset11 import (
            unbind,  # type: ignore[no-redef]
        )
    else:
        from torch.onnx._internal.torchscript_exporter.symbolic_opset13 import (
            unbind,  # type: ignore[no-redef]
        )
    return unbind(g, self, dim, _outputs)

