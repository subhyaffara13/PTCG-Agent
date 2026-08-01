
def get_attn_mask_npu(device):
    """Get or create attention mask for the specified device."""
    if device not in ATTN_MASK_NPU_CACHE:
        ATTN_MASK_NPU_CACHE[device] = torch.triu(torch.ones([2048, 2048], device=device), diagonal=1).bool()
    return ATTN_MASK_NPU_CACHE[device]

