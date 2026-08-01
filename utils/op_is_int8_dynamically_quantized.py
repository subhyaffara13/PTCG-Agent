
def op_is_int8_dynamically_quantized(qconfig) -> bool:
    """Given a qconfig, returns True if this op is using int8 dynamic
    quantization
    """
    activation_dtype, weight_dtype, activation_is_dynamic = get_qconfig_dtypes(qconfig)
    return (
        activation_dtype in [torch.quint8, torch.uint8]
        and
        # for now, the lines below assume fbgemm or qnnpack
        weight_dtype in [torch.qint8, torch.int8]
        and activation_is_dynamic
    )

