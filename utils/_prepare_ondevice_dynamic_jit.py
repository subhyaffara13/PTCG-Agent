
def _prepare_ondevice_dynamic_jit(
    model, qconfig_dict, method_name="forward", inplace=False
):
    return _prepare_ondevice_jit(
        model, qconfig_dict, method_name, inplace, quant_type=QuantType.DYNAMIC
    )

