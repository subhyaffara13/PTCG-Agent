
def _convert_ondevice_dynamic_jit(model, method_name, inplace=False, debug=False):
    return _convert_ondevice_jit(
        model, method_name, inplace, debug, quant_type=QuantType.DYNAMIC
    )

