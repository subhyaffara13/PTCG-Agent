
def is_npu_fa2_top_left_aligned_causal_mask():
    return SPARSE_MODE == TOP_LEFT_ALIGNED_CAUSAL_MASK_MODE if is_torch_npu_available() else False

