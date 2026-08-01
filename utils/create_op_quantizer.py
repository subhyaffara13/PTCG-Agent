
def CreateOpQuantizer(onnx_quantizer, node):  # noqa: N802
    registry = IntegerOpsRegistry if onnx_quantizer.mode == QuantizationMode.IntegerOps else QLinearOpsRegistry
    if node.op_type in registry:
        op_quantizer = registry[node.op_type](onnx_quantizer, node)
        if op_quantizer.should_quantize():
            return op_quantizer
    return QuantOperatorBase(onnx_quantizer, node)

