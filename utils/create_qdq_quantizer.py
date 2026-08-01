
def CreateQDQQuantizer(onnx_quantizer, node):  # noqa: N802
    if node.op_type in QDQRegistry:
        return QDQRegistry[node.op_type](onnx_quantizer, node)
    return QDQOperatorBase(onnx_quantizer, node)

