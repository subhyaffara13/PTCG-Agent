
def _non_vmap_expansion_sdpa(
    batch_indices: torch.Tensor, head_indices: torch.Tensor, q_indices: torch.Tensor, kv_indices: torch.Tensor
):
    """
    Used to broadcast our mask_functions over the all 4 dimensions (b_idx, h_idx, q_idx, kv_idx) of the inputs.
    Allows the usage of any index-based mask function without relying on vmap.

    NOTE: This is limited to index based functions only and is not guaranteed to work otherwise.

    Reference:
        - https://github.com/huggingface/optimum-onnx/blob/c123e8f4fab61b54a8e0e31ce74462bcacca576e/optimum/exporters/onnx/model_patcher.py#L362-L365
    """
    batch_indices = batch_indices[:, None, None, None]
    head_indices = head_indices[None, :, None, None]
    q_indices = q_indices[None, None, :, None]
    kv_indices = kv_indices[None, None, None, :]
    return batch_indices, head_indices, q_indices, kv_indices

