
def _affine_quantize_tensor(weight: torch.Tensor, group_size: int, bits: int):
    """
    Quantize a 2-D float weight ``[N, K]`` into packed uint32 + scales + biases.

    Returns ``(w_packed, scales, biases)`` with:
      - ``w_packed``: ``[N, K // (32 // bits)]`` uint32
      - ``scales``:   ``[N, K // group_size]`` float32/float16/bfloat16
      - ``biases``:   ``[N, K // group_size]`` float32/float16/bfloat16
    """
    N, K = weight.shape
    elems_per_int = 32 // bits
    max_val = (1 << bits) - 1
    n_groups = K // group_size

    w_grouped = weight.float().reshape(N, n_groups, group_size)
    w_min = w_grouped.min(dim=-1).values  # [N, n_groups]
    w_max = w_grouped.max(dim=-1).values

    scales = ((w_max - w_min) / max_val).clamp(min=1e-8)
    biases = w_min

    w_int = (w_grouped - biases.unsqueeze(-1)) / scales.unsqueeze(-1)
    w_int = w_int.round().clamp(0, max_val).to(torch.int32).reshape(N, K)

    # Pack into uint32
    k_packed = K // elems_per_int
    w_packed = torch.zeros(N, k_packed, dtype=torch.int32, device=weight.device)
    for i in range(elems_per_int):
        w_packed |= w_int[:, i::elems_per_int] << (bits * i)

    return w_packed.to(torch.uint32), scales, biases

