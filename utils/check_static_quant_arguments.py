
def check_static_quant_arguments(quant_format: QuantFormat, activation_type: QuantType, weight_type: QuantType):
    if activation_type == QuantType.QInt8 and weight_type == QuantType.QUInt8:
        raise ValueError(
            "ONNXRuntime quantization doesn't support data format:"
            "activation_type=QuantType.QInt8, weight_type=QuantType.QUInt8"
        )
    if activation_type != QuantType.QFLOAT8E4M3FN and weight_type == QuantType.QFLOAT8E4M3FN:
        raise ValueError(
            f"ONNXRuntime quantization doesn't support data format: activation_type={activation_type} "
            "!=QuantType.QFLOAT8E4M3FN, weight_type=QuantType.QFLOAT8E4M3FN."
        )

    if activation_type == QuantType.QFLOAT8E4M3FN and weight_type != QuantType.QFLOAT8E4M3FN:
        raise ValueError(
            "ONNXRuntime quantization doesn't support data format: activation_type=QuantType.QFLOAT8E4M3FN, "
            f"weight_type={weight_type}!=QuantType.QFLOAT8E4M3FN"
        )

    q16_types = [QuantType.QInt16, QuantType.QUInt16]

    if (activation_type in q16_types or weight_type in q16_types) and quant_format != QuantFormat.QDQ:
        raise ValueError("Only QuantFormat.QDQ supports 16-bit quantization types.")

    if activation_type == QuantType.QInt8 and weight_type == QuantType.QInt8 and quant_format != QuantFormat.QDQ:
        logging.warning(
            "Please use QuantFormat.QDQ for activation type QInt8 and weight type QInt8. "
            "Or it will lead to bad performance on x64."
        )

