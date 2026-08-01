
def _group_quantize_tensor_symmetric(w, n_bit=4, groupsize=32):
    # W is of shape [K x N]
    # We transpose W as Quantization is applied on [N x K]
    w = w.transpose(0, 1).contiguous()
    if w.dim() != 2:
        raise AssertionError(f"Expected w.dim() == 2, got {w.dim()}")
    if groupsize <= 1:
        raise AssertionError(f"Expected groupsize > 1, got {groupsize}")
    if w.shape[-1] % groupsize != 0:
        raise AssertionError(f"Expected w.shape[-1] % groupsize == 0, got {w.shape[-1]} % {groupsize}")
    # Calculate scale and zeros
    to_quant = w.reshape(-1, groupsize)
    max_val = to_quant.abs().amax(dim=1, keepdim=True)
    eps = torch.finfo(max_val.dtype).eps
    max_int = 2 ** (n_bit - 1) - 1  # For 4-bit, this is 7
    scales = max_val.clamp(min=eps) / max_int
    zeros = torch.zeros_like(scales)

    # Quantize the weight
    scales = scales.to(torch.float32).reshape(w.shape[0], -1)
    zeros = zeros.to(torch.float32).reshape(w.shape[0], -1)
    scales = scales.reshape(-1, 1)
    zeros = zeros.reshape(-1, 1)
    max_int = 2**n_bit - 1
    w_int8 = to_quant.div(scales).add(8.5).to(torch.int8).clamp(max=max_int)
    # We pack 2 signed int4 values in unsigned uint8 container.
    # This reduces the weight size by half and improves load perf
    out_uint8 = (w_int8[::, 1::2] << 4 | w_int8[::, ::2]).to(torch.uint8)

    scales_and_zeros = scales.squeeze().contiguous()

    return out_uint8, scales_and_zeros

