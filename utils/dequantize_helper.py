
def dequantize_helper(
    g: jit_utils.GraphContext,
    qtensor: _C.Value,
    qdtype: _C_onnx.TensorProtoDataType | None = None,
) -> tuple[_C.Value, _C.Value, _C.Value, _C.Value | None]:
    """Appends to graph `g` ONNX nodes that dequantizes `qtensor` into `tensor`.

    Args:
        g: Graph, the ONNX IR graph that is under construction.
        qtensor: torch._C.Value, either a tuple of (quantized_tensor, scale, zero_point)
            for per tensor quantization, or
            (quantized_tensor, scale, zero_point, axis) for per channel quantization,
            representing the quantized tensor.
        qdtype: torch.onnx.TensorProtoDataType default None, if not None, represents the
            data type of quantized tensor. It must be either
            torch.onnx.TensorProtoDataType.UINT8 or torch.onnx.TensorProtoDataType.INT8.
    """
    unpacked_qtensors = _unpack_quantized_tensor(qtensor)
    tensor, scale, zero_point = unpacked_qtensors[:3]
    axis = unpacked_qtensors[3] if len(unpacked_qtensors) >= 4 else None
    axis_i = _get_const(axis, "i", "axis")
    input_qdtype = _type_utils.JitScalarType.from_value(tensor)
    if qdtype is None:
        if input_qdtype is not None:
            qdtype = input_qdtype.onnx_type()
        else:
            qdtype = _C_onnx.TensorProtoDataType.UINT8
    value = g.op("Cast", tensor, to_i=qdtype)
    scale = g.op("Cast", scale, to_i=_C_onnx.TensorProtoDataType.FLOAT)
    zero_point = g.op("Cast", zero_point, to_i=qdtype)

    if axis_i is not None and GLOBALS.export_onnx_opset_version < 13:
        _onnx_opset_unsupported_detailed(
            "DequantizeLinear",
            GLOBALS.export_onnx_opset_version,
            13,
            "Attribute axis is not supported.",
            qtensor,
        )

    return (
        g.op("DequantizeLinear", value, scale, zero_point, axis_i=axis_i),
        scale,
        zero_point,
        axis,
    )

