
def flash_attn_supports_top_left_mask():
    if is_flash_attn_2_available() or is_flash_attn_3_available() or is_flash_attn_4_available():
        return False

    from .integrations.npu_flash_attention import is_npu_fa2_top_left_aligned_causal_mask

    return is_npu_fa2_top_left_aligned_causal_mask()

