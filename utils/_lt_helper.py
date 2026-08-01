
def _lt_helper(g: jit_utils.GraphContext, input, other):
    if g.opset <= 8:
        from torch.onnx._internal.torchscript_exporter.symbolic_opset8 import lt as _lt8

        return _lt8(g, input, other)
    else:
        from torch.onnx._internal.torchscript_exporter.symbolic_opset9 import lt as _lt9

        return _lt9(g, input, other)

