
def _elementwise_output_like(*inputs, dtype):
    from torch._prims_common import compute_elementwise_output_logical_to_physical_perm

    broadcasted = torch.broadcast_tensors(*inputs)
    l2p_perm, _ = compute_elementwise_output_logical_to_physical_perm(*broadcasted)
    return torch.empty_permuted(
        broadcasted[0].shape, l2p_perm, dtype=dtype, device=broadcasted[0].device
    )

