
def _interpolate_get_scales_if_available(g: jit_utils.GraphContext, scales):
    available_scales = _maybe_get_const(scales[0], "fs") != -1 and not _is_none(
        scales[0]
    )

    if not available_scales:
        return None

    offsets = g.op("Constant", value_t=torch.ones(2, dtype=torch.float32))
    scales_list = g.op(
        "Constant", value_t=torch.tensor(_maybe_get_const(scales[0], "fs"))
    )
    scales = g.op("Concat", offsets, scales_list, axis_i=0)
    return scales

