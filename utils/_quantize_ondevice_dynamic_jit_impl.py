
def _quantize_ondevice_dynamic_jit_impl(
    model, qconfig_dict, method_name, inplace=False
):
    model = _prepare_ondevice_dynamic_jit(model, qconfig_dict, method_name, inplace)
    model = _convert_ondevice_dynamic_jit(model, method_name, inplace)
    return model

