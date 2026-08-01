
def pack_weight_bias(qweight, bias, dtype):
    if dtype == torch.qint8:
        # for each layer, for each direction we need to quantize and pack
        # weights and pack parameters in this order:
        #
        #   w_ih, w_hh
        packed_weight = torch.ops.quantized.linear_prepack(qweight, bias)

        return packed_weight
    else:
        # for each layer, for each direction we need to quantize and pack
        # weights and pack parameters in this order:
        #
        #   packed_ih, packed_hh, b_ih, b_hh
        packed_weight = torch.ops.quantized.linear_prepack_fp16(qweight, bias)

        return packed_weight

