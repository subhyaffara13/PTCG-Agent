
def _pad_circular(g: jit_utils.GraphContext, input: _C.Value, pad: _C.Value):
    padding = _convert_padding_node(pad)
    if len(padding) % 2 != 0:
        raise AssertionError(f"padding length must be even, got {len(padding)}")
    ndim = len(padding) // 2

    cur = input
    for idx in range(ndim):
        pad_r = padding[-(2 * idx + 1)]
        pad_l = padding[-(2 * idx + 2)]
        tensors = []
        if pad_l > 0:
            left = symbolic_helper._slice_helper(
                g, cur, axes=[2 + idx], starts=[-(pad_l)], ends=[_constants.INT64_MAX]
            )
            tensors.append(left)

        if pad_l < 0 or pad_r < 0:
            start = builtins.max(0, -pad_l)
            end = -(builtins.max(0, -pad_r))
            middle = symbolic_helper._slice_helper(
                g,
                cur,
                axes=[2 + idx],
                starts=[start],
                ends=[end],
            )
            tensors.append(middle)
        else:
            tensors.append(cur)

        if pad_r > 0:
            right = symbolic_helper._slice_helper(
                g, cur, axes=[2 + idx], starts=[0], ends=[pad_r]
            )
            tensors.append(right)

        cur = g.op("Concat", *tensors, axis_i=(2 + idx))

    return cur

