
def convert_jit(model, inplace=False, debug=False, preserved_attrs=None):
    torch._C._log_api_usage_once("quantization_api.quantize_jit.convert_jit")
    return _convert_jit(
        model,
        inplace,
        debug,
        quant_type=QuantType.STATIC,
        preserved_attrs=preserved_attrs,
    )

