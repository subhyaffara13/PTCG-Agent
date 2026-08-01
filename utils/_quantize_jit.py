
def _quantize_jit(
    model,
    qconfig_dict,
    run_fn=None,
    run_args=None,
    inplace=False,
    debug=False,
    quant_type=QuantType.STATIC,
):
    # Always do inplace convert because the Tensor is already
    # copied in prepare_jit when inplace is False
    if quant_type == QuantType.DYNAMIC:
        model = prepare_dynamic_jit(model, qconfig_dict, inplace)
        model = convert_dynamic_jit(model, True, debug)
    else:
        if not run_fn:
            raise AssertionError(
                "Must provide calibration function for post training static quantization"
            )
        if not run_args:
            raise AssertionError(
                "Must provide calibration dataset for post training static quantization"
            )
        model = prepare_jit(model, qconfig_dict, inplace)
        run_fn(model, *run_args)
        model = convert_jit(model, True, debug)

    torch._C._jit_pass_constant_propagation(model.graph)
    torch._C._jit_pass_dce(model.graph)
    return model

