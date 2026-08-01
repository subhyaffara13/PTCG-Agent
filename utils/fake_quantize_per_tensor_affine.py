
def fake_quantize_per_tensor_affine(
    g: jit_utils.GraphContext,
    inputs,
    scale,
    zero_point,
    quant_min=-128,
    quant_max=127,
):
    # NOTE: (0, 127) is a special case. PyTorch restricts activations to be in the range (0, 127).
    #   https://github.com/pytorch/pytorch/blob/b34b192d6b97325c9f78e5995c48c8498ede34bd/torch/ao/quantization/observer.py#L1422
    if (quant_min, quant_max) == (0, 127):
        symbolic_helper._onnx_opset_unsupported_detailed(
            "fake_quantize_per_tensor_affine",
            10,
            13,
            "Quantize range (0, 127) not supported, requires opset 13 Clip",
            inputs,
        )
    if (quant_min, quant_max) not in [(0, 255), (-128, 127)]:
        raise errors.SymbolicValueError(
            f"For (quant_min, quant_max), ONNX allows only (0, 255) and (-128, 127). "
            f"Got ({quant_min}, {quant_max})",
            inputs,
        )
    scale = symbolic_helper._maybe_get_scalar(scale)
    if scale is None:
        symbolic_helper._onnx_opset_unsupported_detailed(
            "fake_quantize_per_tensor_affine",
            10,
            13,
            "Non-constant scale not supported",
            inputs,
        )

    scale = scale.float().data  # Avoid exporter generating double type
    if quant_min == 0:
        zero_point = g.op("Cast", zero_point, to_i=_C_onnx.TensorProtoDataType.UINT8)
    else:
        zero_point = g.op("Cast", zero_point, to_i=_C_onnx.TensorProtoDataType.INT8)
    return g.op(
        "DequantizeLinear",
        g.op("QuantizeLinear", inputs, scale, zero_point),
        scale,
        zero_point,
    )


def fake_quantize_per_tensor_affine(
    g: jit_utils.GraphContext,
    inputs,
    scale,
    zero_point,
    quant_min=-128,
    quant_max=127,
):
    # NOTE: (0, 127) is allowed as special case. PyTorch restricts activations to be in the range (0, 127).
    #   https://github.com/pytorch/pytorch/blob/b34b192d6b97325c9f78e5995c48c8498ede34bd/torch/ao/quantization/observer.py#L1422
    if (quant_min, quant_max) not in [(0, 255), (-128, 127), (0, 127)]:
        raise errors.SymbolicValueError(
            "For (quant_min, quant_max), ONNX allows only (0, 127), (0, 255) and (-128, 127). "
            f"Got ({quant_min}, {quant_max})",
            inputs,
        )
    if quant_min == 0:
        zero_point = g.op("Cast", zero_point, to_i=_C_onnx.TensorProtoDataType.UINT8)
    else:
        zero_point = g.op("Cast", zero_point, to_i=_C_onnx.TensorProtoDataType.INT8)
    if (
        _type_utils.JitScalarType.from_value(scale, _type_utils.JitScalarType.UNDEFINED)
        != _type_utils.JitScalarType.FLOAT
    ):
        scale = g.op("Cast", scale, to_i=_C_onnx.TensorProtoDataType.FLOAT)
    quantized = g.op("QuantizeLinear", inputs, scale, zero_point)
    if (quant_min, quant_max) == (0, 127):
        quantized = g.op(
            "Clip",
            quantized,
            opset9.unused(g),
            g.op("Constant", value_t=torch.tensor(127, dtype=torch.uint8)),
        )
    return g.op("DequantizeLinear", quantized, scale, zero_point)

