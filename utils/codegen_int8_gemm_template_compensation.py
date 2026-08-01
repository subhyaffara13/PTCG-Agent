
def codegen_int8_gemm_template_compensation(
    use_int8_fast_compensation_path: bool,
    input: OpsValue,
    _weight_compo: OpsValue,
    _x_scale: OpsValue | None,
    _x_zp: OpsValue | None,
    _w_scale: OpsValue | None,
    _x_w_scale: OpsValue | None,
) -> OpsValue:
    if use_int8_fast_compensation_path:
        temp = ops.sub(
            ops.mul(
                input,
                _x_w_scale,
            ),
            _weight_compo,
        )
    else:
        temp = ops.mul(
            ops.mul(
                input,
                _x_scale,
            ),
            _w_scale,
        )
        # NOTE: We will apply compensation even if the x_zp is 0 for int8 quantization.
        # That's because when torch.compile is invoked for dynamic quantization,
        # x might coincidentally have such values that x_zp might be zero despite
        # asymmetric quantization.
        # Besides, if x_zp is dummy for int8 x, or if x is statically quantized,
        # we'd still perform that redundant compute to avoid making the code messy
        # because we discovered that redundant computation of compensation did not
        # lead to performance degradation with the input shapes tested.
        temp = ops.sub(
            temp,
            ops.mul(
                ops.mul(
                    ops.mul(
                        _x_scale,
                        _w_scale,
                    ),
                    _x_zp,
                ),
                _weight_compo,
            ),
        )
    return temp

