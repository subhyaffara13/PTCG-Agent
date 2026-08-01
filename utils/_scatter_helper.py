
def _scatter_helper(g: jit_utils.GraphContext, self, dim, index, src):
    if g.opset <= 10:
        from torch.onnx._internal.torchscript_exporter.symbolic_opset9 import scatter
    else:
        # for mypy, scatter was imported two lines above
        from torch.onnx._internal.torchscript_exporter.symbolic_opset11 import (
            scatter,  # type: ignore[no-redef]
        )
    return scatter(g, self, dim, index, src)

