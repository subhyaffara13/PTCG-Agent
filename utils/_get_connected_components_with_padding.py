
def _get_connected_components_with_padding(mask):
    """Get connected components from masks (possibly padding them to an even size)."""
    mask = mask.to(torch.uint8)
    _, _, H, W = mask.shape

    # Try to use kernels for connected components, fallback if unavailable
    _load_cv_utils_kernel_once()
    if not cv_utils_kernel:
        # Fallback: return dummy labels and counts that won't trigger filtering
        labels = torch.zeros_like(mask, dtype=torch.int32)
        counts = torch.full_like(mask, fill_value=mask.shape[2] * mask.shape[3] + 1, dtype=torch.int32)
        return labels, counts

    # make sure both height and width are even (to be compatible with cc_torch)
    pad_h = H % 2
    pad_w = W % 2

    try:
        if pad_h == 0 and pad_w == 0:
            labels, counts = cv_utils_kernel.cc_2d(mask.contiguous(), get_counts=True)
        else:
            # pad the mask to make its height and width even
            # padding format is (padding_left,padding_right,padding_top,padding_bottom)
            mask_pad = F.pad(mask, (0, pad_w, 0, pad_h), mode="constant", value=0)
            labels, counts = cv_utils_kernel.cc_2d(mask_pad.contiguous(), get_counts=True)
            labels = labels[:, :, :H, :W]
            counts = counts[:, :, :H, :W]
    except Exception as e:
        logger.warning_once(
            f"Failed to compute connected components using kernels library: {e}. "
            "Hole filling and sprinkle removal will be skipped."
        )
        # Fallback: return dummy labels and counts that won't trigger filtering
        labels = torch.zeros_like(mask, dtype=torch.int32)
        counts = torch.full_like(mask, fill_value=H * W + 1, dtype=torch.int32)
        return labels, counts

    return labels, counts

