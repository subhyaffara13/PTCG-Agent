
def _pad_packed_sequence(
    g: jit_utils.GraphContext,
    data,
    batch_sizes,
    batch_first,
    padding_value,
    total_length,
):
    # Ignore total_length as it is not supported in _symbolic_pad_packed_sequence
    # It is only useful/used when training using data_parallel model, so
    # It shouldn't be relevant for ONNX anyway
    data, lengths = g.op("prim::PadPacked", data, batch_sizes, outputs=2)
    if batch_first:
        data = g.op("Transpose", data, perm_i=[1, 0, 2])
    return data, lengths

