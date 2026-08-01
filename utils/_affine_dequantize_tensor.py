
def _affine_dequantize_tensor(
    w_packed: torch.Tensor, scales: torch.Tensor, biases: torch.Tensor, group_size: int, bits: int
):
    """
    Dequantize a packed uint32 weight ``[N, K_packed]`` back to float.

    Returns a ``[N, K]`` float32 tensor.
    """
    N = w_packed.shape[0]
    elems_per_int = 32 // bits
    max_val = (1 << bits) - 1
    K = w_packed.shape[1] * elems_per_int

    w_packed_i = w_packed.to(torch.int32)
    w_flat = torch.zeros(N, K, dtype=torch.float32, device=w_packed.device)
    for i in range(elems_per_int):
        w_flat[:, i::elems_per_int] = ((w_packed_i >> (bits * i)) & max_val).float()

    w_grouped = w_flat.reshape(N, -1, group_size)
    w_deq = w_grouped * scales.float().unsqueeze(-1) + biases.float().unsqueeze(-1)
    return w_deq.reshape(N, K)

